import logging
from flask import send_file
from flask import Blueprint
import os

PWD = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
pages_bp = Blueprint('pages', __name__, url_prefix='/')


def serve_static_html(filename):
    """Helper function to serve static HTML files"""
    return send_file(os.path.join(PWD, f"../statics/{filename}.html"))


@pages_bp.get('/')
def get_index():
    return serve_static_html("index")

@pages_bp.get("/FolderBrowser")
def get_folder_browser():
    return serve_static_html("FolderBrowser")

@pages_bp.get("/Table")
def get_tabular_slice_dice():
    return serve_static_html("Table")


@pages_bp.get("/api/health")
def healthchecker():
    return {"status": "success", "message": "SenseTable is running"}







