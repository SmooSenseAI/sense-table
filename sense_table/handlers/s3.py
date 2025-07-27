import os
from urllib.parse import urlparse
import logging
from flask import Blueprint, jsonify, request, redirect, current_app
import textwrap

logger = logging.getLogger(__name__)
s3_bp = Blueprint('s3', __name__)

@s3_bp.route('/s3-proxy')
def proxy():
    url = request.args.get('url')    
    try:
        # Get s3_client from app config
        s3_client = current_app.config['S3_CLIENT']
        
        # Parse the S3 URL
        parsed = urlparse(url)
        if parsed.scheme == 's3':
            bucket = parsed.netloc
            key = parsed.path.lstrip('/')
            signed_url = s3_client.generate_presigned_url(
                'get_object', 
                Params={
                    'Bucket': bucket, 
                    'Key': key,
                    # S3 inconsistently omitting CORS headers for cached presigned responses when no response overrides are used.
                    'ResponseCacheControl': 'no-cache',
                    'ResponseContentDisposition': 'inline',
                }, ExpiresIn=3600)
            return redirect(signed_url)
        else:
            raise NotImplementedError(textwrap.dedent(f"""
                Unsupported URL scheme: {parsed.scheme}. 
                You can implement your own proxy by overriding app.view_functions['s3.proxy'] = func
                """))

    except Exception as e:
        logger.error(f"Error generating signed URL for {url}: {str(e)}")
        return jsonify({'error': str(e)}), 500

    