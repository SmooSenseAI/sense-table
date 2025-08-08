import unittest
import threading
import time
import logging
import os
from playwright_utils import PlaywrightTestMixin, BASE_URL, DATA_DIR
from sense_table.app import SenseTableApp
import pandas
from sense_table.utils.duckdb_connections import duckdb_connection_using_s3
import boto3


PWD = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)


class BaseTestCase(unittest.TestCase, PlaywrightTestMixin):
    """
    Base test case class for integration tests that need a running server.

    This class automatically handles:
    - Server startup before tests begin
    - Server cleanup after tests complete
    - Playwright utilities for browser testing

    Usage:
        class TestMyFeature(BaseTestCase):
            def test_my_feature(self):
                with playwright_page() as page:
                    page.goto("http://localhost:8000/my-endpoint")
                    # Your test code here
    """

    server_thread = None
    app_instance = None
    _server_started = False

    @classmethod
    def setUpClass(cls):
        """Start the server in a separate thread before running tests"""
        if cls._server_started:
            logger.info("Server already started, skipping startup")
            return

        logger.info("Starting server for integration tests...")

        # Create the app instance
        cls.app_instance = SenseTableApp(duckdb_connection_maker=duckdb_connection_using_s3(s3_client=boto3.client('s3')),)
        flask_app = cls.app_instance.create_app()

        # Configure Flask for testing
        flask_app.config['TESTING'] = True

        def run_server():
            try:
                # Run the server (this will block)
                flask_app.run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)
            except Exception as e:
                logger.error(f"Server failed to start: {e}")

        # Start server in a separate thread
        cls.server_thread = threading.Thread(target=run_server, daemon=True)
        cls.server_thread.start()

        # Wait a bit for server to start
        time.sleep(2)

        # Verify server is running by making a simple request
        import requests
        try:
            response = requests.get(f"{BASE_URL}/api/settings", timeout=5)
            if response.status_code == 200:
                logger.info("Server started successfully")
                cls._server_started = True
            else:
                raise Exception(f"Server responded with status {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to verify server startup: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Clean up the server after tests"""
        if not cls._server_started:
            return

        logger.info("Shutting down server...")

        # Since Flask's development server doesn't have a clean shutdown method,
        # and we're using daemon threads, the server will automatically terminate
        # when the main process exits. For more robust shutdown, you could
        # implement a proper shutdown mechanism or use a production WSGI server.

        if cls.server_thread and cls.server_thread.is_alive():
            logger.info("Server thread will terminate with main process")

        cls._server_started = False

