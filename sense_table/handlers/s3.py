import os
from urllib.parse import urlparse
import logging
from flask import Blueprint, jsonify, request, redirect, current_app
import textwrap
from sense_table.utils.s3_fs import S3FileSystem

logger = logging.getLogger(__name__)
s3_bp = Blueprint('s3', __name__)

@s3_bp.route('/s3-proxy')
def proxy():
    url = request.args.get('url')    
    try:
        # Get s3_client from app config
        s3_client = current_app.config['S3_CLIENT']
        
        signed_url = S3FileSystem(s3_client).sign_get_url(url)
        return redirect(signed_url)

    except Exception as e:
        logger.error(f"Error generating signed URL for {url}: {str(e)}")
        return jsonify({'error': str(e)}), 500

    