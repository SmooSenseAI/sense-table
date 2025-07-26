from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import os
import logging
from sense_table.query import query_bp
from sense_table.local_file_system import fs_bp
from sense_table.pages import pages_bp
from sense_table.s3 import s3_bp
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
        s3_client: boto3.client = boto3.client('s3'),
    ):
        self.settings = settings
        self.s3_client = s3_client

    def create_app(self):
        app = Flask(__name__, static_folder='statics', static_url_path='/')
        CORS(app)
        
        # Store the s3_client in app config so blueprints can access it
        app.config['S3_CLIENT'] = self.s3_client
        
        app.register_blueprint(query_bp)
        app.register_blueprint(fs_bp)
        app.register_blueprint(pages_bp)
        app.register_blueprint(s3_bp)
        
        @app.route('/api/settings')
        def get_settings():
            return jsonify(self.settings.model_dump())
        
        return app
    
    def run(self, host: str = '0.0.0.0', port: int = 8000):
        self.create_app().run(host=host, port=port)


if __name__ == "__main__":
    SenseTableApp().run()
