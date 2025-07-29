from flask import Flask, jsonify
import os
import logging
from sense_table.handlers.query import query_bp
from sense_table.handlers.fs import fs_bp
from sense_table.handlers.pages import pages_bp
from sense_table.handlers.s3 import s3_bp
from sense_table.settings import SenseTableSettings
from pydantic import validate_call
import boto3
PWD = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger(__name__)

class SenseTableApp:
    @validate_call
    def __init__(
        self, *, 
        settings: SenseTableSettings = SenseTableSettings(),
        url_prefix: str = '',
        s3_client: boto3.client = boto3.client('s3'),
    ):
        self.settings = settings
        self.s3_client = s3_client
        if url_prefix:
            assert url_prefix.startswith('/'), "url_prefix must start with /"
            assert not url_prefix.endswith('/'), "url_prefix must not end with /"
        self.url_prefix = url_prefix
        
    def create_app(self):
        app = Flask(__name__, static_folder='statics', static_url_path=f'{self.url_prefix}')
        
        # Store the s3_client in app config so blueprints can access it
        app.config['S3_CLIENT'] = self.s3_client
        app.config['URL_PREFIX'] = self.url_prefix
        
        # Register blueprints with url_prefix
        app.register_blueprint(query_bp, url_prefix=f"{self.url_prefix}/api")
        app.register_blueprint(fs_bp, url_prefix=f"{self.url_prefix}/api")
        app.register_blueprint(pages_bp, url_prefix=self.url_prefix)
        app.register_blueprint(s3_bp, url_prefix=f"{self.url_prefix}/api")
        
        @app.route(f'{self.url_prefix}/api/settings')
        def get_settings():
            return jsonify(self.settings.model_dump())
        
        return app
    
    def run(self, host: str = '0.0.0.0', port: int = 8000):
        self.create_app().run(host=host, port=port)


if __name__ == "__main__":
    SenseTableApp(
        url_prefix='',
        settings=SenseTableSettings(
            enableDebugging=True,
        )
    ).run()
