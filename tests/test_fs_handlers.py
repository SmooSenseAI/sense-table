import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import json
from flask import Flask
from sense_table.handlers.fs import fs_bp, get_ls
from sense_table.utils.models import FSItem
from my_logging import getLogger

logger = getLogger(__name__)

class TestFSHandlers(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = Flask(__name__)
        self.app.register_blueprint(fs_bp)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

        # Create some test files and directories
        self.test_file = os.path.join(self.temp_dir, 'test_file.txt')
        self.test_dir = os.path.join(self.temp_dir, 'test_dir')

        with open(self.test_file, 'w') as f:
            f.write('test content')

        os.makedirs(self.test_dir, exist_ok=True)

        # Create a hidden file
        self.hidden_file = os.path.join(self.temp_dir, '.hidden_file')
        with open(self.hidden_file, 'w') as f:
            f.write('hidden content')

        # Set up application context for all tests
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test method."""
        import shutil
        # Pop the application context
        self.app_context.pop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_ls_local_path_success(self):
        """Test successful listing of local directory."""
        with self.app.test_request_context(f'/ls?path={self.temp_dir}'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

            # Check that we get the expected items
            names = [item['name'] for item in data]
            self.assertIn('test_file.txt', names)
            self.assertIn('test_dir', names)

            # Check that items have the expected structure
            for item in data:
                self.assertIn('name', item)
                self.assertIn('size', item)
                self.assertIn('lastModified', item)
                self.assertIn('isDir', item)

    def test_get_ls_with_limit(self):
        """Test listing with limit parameter."""
        # Create additional files to test limit
        for i in range(5):
            with open(os.path.join(self.temp_dir, f'file_{i}.txt'), 'w') as f:
                f.write(f'content {i}')

        with self.app.test_request_context(f'/ls?path={self.temp_dir}&limit=3'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(data), 3)

    def test_get_ls_show_hidden_false(self):
        """Test that hidden files are excluded by default."""
        with self.app.test_request_context(f'/ls?path={self.temp_dir}&show_hidden=false'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            names = [item['name'] for item in data]
            self.assertNotIn('.hidden_file', names)

    def test_get_ls_show_hidden_true(self):
        """Test that hidden files are included when show_hidden=true."""
        with self.app.test_request_context(f'/ls?path={self.temp_dir}&show_hidden=true'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            names = [item['name'] for item in data]
            self.assertIn('.hidden_file', names)

    def test_get_ls_nonexistent_path(self):
        """Test error handling for nonexistent path."""
        nonexistent_path = '/nonexistent/path/12345'
        with self.app.test_request_context(f'/ls?path={nonexistent_path}'):
            response = get_ls()
            self.assertIsInstance(response, tuple)
            self.assertEqual(response[1], 400)  # status code
            data = json.loads(response[0].get_data(as_text=True))
            self.assertIn('error', data)
            self.assertIn('does not exist', data['error'])

    def test_get_ls_missing_path_parameter(self):
        """Test error handling when path parameter is missing."""
        with self.app.test_request_context('/ls'):
            response = get_ls()
            # When path is None, it will cause an AttributeError in the function
            # which should be caught and return an error response
            self.assertIsInstance(response, tuple)
            self.assertEqual(response[1], 400)  # status code
            data = json.loads(response[0].get_data(as_text=True))
            self.assertIn('error', data)

    @patch('sense_table.handlers.fs.S3FileSystem')
    @patch('sense_table.handlers.fs.current_app')
    def test_get_ls_s3_path(self, mock_current_app, mock_s3_fs_class):
        """Test listing S3 path."""
        # Mock S3 client and file system
        mock_s3_client = Mock()
        mock_current_app.config = {'S3_CLIENT': mock_s3_client}

        mock_s3_fs = Mock()
        mock_s3_fs_class.return_value = mock_s3_fs

        # Mock FSItem objects
        mock_items = [
            FSItem(name='s3_file1.txt', size=100, lastModified=1234567890, isDir=False),
            FSItem(name='s3_dir1', size=0, lastModified=1234567890, isDir=True)
        ]
        mock_s3_fs.list_one_level.return_value = mock_items

        with self.app.test_request_context('/ls?path=s3://bucket/path'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)

            # Verify S3FileSystem was called correctly
            mock_s3_fs_class.assert_called_once_with(mock_s3_client)
            mock_s3_fs.list_one_level.assert_called_once_with('s3://bucket/path', 100)

    @patch('sense_table.handlers.fs.S3FileSystem')
    @patch('sense_table.handlers.fs.current_app')
    def test_get_ls_s3_with_limit(self, mock_current_app, mock_s3_fs_class):
        """Test S3 listing with custom limit."""
        mock_s3_client = Mock()
        mock_current_app.config = {'S3_CLIENT': mock_s3_client}

        mock_s3_fs = Mock()
        mock_s3_fs_class.return_value = mock_s3_fs
        mock_s3_fs.list_one_level.return_value = []

        with self.app.test_request_context('/ls?path=s3://bucket/path&limit=50'):
            response = get_ls()

            self.assertEqual(response.status_code, 200)
            mock_s3_fs.list_one_level.assert_called_once_with('s3://bucket/path', 50)

    @patch('sense_table.handlers.fs.S3FileSystem')
    @patch('sense_table.handlers.fs.current_app')
    def test_get_ls_s3_error(self, mock_current_app, mock_s3_fs_class):
        """Test S3 error handling."""
        mock_s3_client = Mock()
        mock_current_app.config = {'S3_CLIENT': mock_s3_client}

        mock_s3_fs = Mock()
        mock_s3_fs_class.return_value = mock_s3_fs
        mock_s3_fs.list_one_level.side_effect = Exception("S3 connection failed")

        with self.app.test_request_context('/ls?path=s3://bucket/path'):
            response = get_ls()
            self.assertIsInstance(response, tuple)
            self.assertEqual(response[1], 400)  # status code
            data = json.loads(response[0].get_data(as_text=True))
            self.assertIn('error', data)
            self.assertIn('S3 connection failed', data['error'])

    def test_get_ls_invalid_limit_parameter(self):
        """Test error handling for invalid limit parameter."""
        with self.app.test_request_context(f'/ls?path={self.temp_dir}&limit=invalid'):
            # The current implementation doesn't handle invalid limit parameters
            # This test documents the current behavior - it will raise a ValueError
            with self.assertRaises(ValueError):
                get_ls()

    def test_get_ls_directory_structure(self):
        """Test that directory items are correctly identified."""
        with self.app.test_request_context(f'/ls?path={self.temp_dir}'):
            response = get_ls()
            data = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)

            # Find the directory item
            dir_item = next((item for item in data if item['name'] == 'test_dir'), None)
            self.assertIsNotNone(dir_item)
            self.assertTrue(dir_item['isDir'])
            # Directory size can vary by filesystem, so just check it's a number
            self.assertIsInstance(dir_item['size'], int)

            # Find the file item
            file_item = next((item for item in data if item['name'] == 'test_file.txt'), None)
            self.assertIsNotNone(file_item)
            self.assertFalse(file_item['isDir'])
            self.assertGreater(file_item['size'], 0)

    def test_get_ls_via_blueprint_route(self):
        """Test the get_ls function through the Flask blueprint route."""
        response = self.client.get(f'/ls?path={self.temp_dir}')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

        # Verify we get the expected items
        names = [item['name'] for item in data]
        self.assertIn('test_file.txt', names)
        self.assertIn('test_dir', names)


if __name__ == '__main__':
    unittest.main()
