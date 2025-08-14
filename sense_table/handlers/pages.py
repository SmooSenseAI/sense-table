import json
import logging
import os
import textwrap

from flask import Blueprint, Response, current_app, jsonify, redirect, request
from werkzeug.wrappers import Response as WerkzeugResponse

from sense_table.utils.s3_fs import S3FileSystem

PWD = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
pages_bp = Blueprint("pages", __name__)


def serve_static_html(filename: str) -> Response:
    """Helper function to serve static HTML files"""
    url_prefix = current_app.config.get("URL_PREFIX", "")
    state_file = request.args.get("state")
    template_file_path = os.path.join(PWD, f"../statics/{filename}.html")
    with open(template_file_path) as f:
        content = f.read()
    state_data = {}
    if state_file:
        # Get the S3 client from Flask app config
        s3_client = current_app.config["S3_CLIENT"]
        s3_fs = S3FileSystem(s3_client)
        try:
            state_content = s3_fs.read_text_file(state_file)
            if state_content:
                state_data = json.loads(state_content)
        except Exception as e:
            logger.exception(f"Failed to read state file from S3: {e}")

    content = content.replace(
        "<head>",
        textwrap.dedent(f'''
        <head>
        <script>
            const URL_PREFIX = "{url_prefix}";
            const PRE_LOADED_STATE = {json.dumps(state_data)};
        </script>
        </head>'''),
    )
    return Response(content, mimetype="text/html")


@pages_bp.get("/")
def get_index() -> WerkzeugResponse:
    url_prefix = current_app.config.get("URL_PREFIX", "")
    redirect_url = os.path.join(url_prefix, "FolderBrowser")
    return redirect(redirect_url)


@pages_bp.get("/FolderBrowser")
def get_folder_browser() -> Response:
    return serve_static_html("FolderBrowser")


@pages_bp.get("/Table")
def get_tabular_slice_dice() -> Response:
    return serve_static_html("Table")


@pages_bp.get("/MainTable")
def get_main_table() -> Response:
    return serve_static_html("MainTable")


@pages_bp.get("/api/health")
def healthchecker() -> Response:
    return jsonify({"status": "success", "message": "SenseTable is running"})
