import logging

from flask import Blueprint, current_app, jsonify, redirect, request

from sense_table.utils.s3_fs import S3FileSystem

logger = logging.getLogger(__name__)
s3_bp = Blueprint("s3", __name__)


@s3_bp.get("/s3-proxy")
def proxy():
    url = request.args.get("url")
    try:
        # Get s3_client from app config
        s3_client = current_app.config["S3_CLIENT"]

        signed_url = S3FileSystem(s3_client).sign_get_url(url)
        return redirect(signed_url)

    except Exception as e:
        logger.error(f"Error generating signed URL for {url}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@s3_bp.post("/s3-proxy")
def batch_proxy():
    urls = request.json.get("urls")
    try:
        # Get s3_client from app config
        s3_client = current_app.config["S3_CLIENT"]
        s3_fs = S3FileSystem(s3_client)
        signed = [s3_fs.sign_get_url(url) for url in urls]
        return jsonify(signed)
    except Exception as e:
        logger.error(f"Error generating signed URLs for {urls}: {str(e)}")
        return jsonify({"error": str(e)}), 500
