import logging
import os
import pathlib

from botocore.exceptions import ClientError
from flask import Blueprint, current_app, jsonify, redirect, request, send_file
from werkzeug.wrappers import Response

from sense_table.exceptions import AccessDeniedException, InvalidInputException
from sense_table.utils.api import handle_api_errors, require_arg
from sense_table.utils.local_fs import LocalFileSystem
from sense_table.utils.s3_fs import S3FileSystem

logger = logging.getLogger(__name__)
fs_bp = Blueprint("fs", __name__)


@fs_bp.get("/ls")
@handle_api_errors
def get_ls() -> Response:
    path = require_arg("path")
    limit = int(request.args.get("limit", 100))
    show_hidden = request.args.get("show_hidden", "false").lower() == "true"
    if path.startswith("s3://"):
        s3_client = current_app.config["S3_CLIENT"]
        items = S3FileSystem(s3_client).list_one_level(path, limit)
    else:
        items = LocalFileSystem.list_one_level(path, limit, show_hidden)
    return jsonify([item.model_dump() for item in items])


@fs_bp.get("/get-file")
@handle_api_errors
def get_file() -> Response:
    path = require_arg("path")
    ext = os.path.splitext(path)[1]
    mime_type = {
        ".json": "application/json",
        ".txt": "text/plain",
    }
    if path.startswith("s3://"):
        logger.info(f"Generating signed URL for {path}")
        s3_client = current_app.config["S3_CLIENT"]
        signed_url = S3FileSystem(s3_client).sign_get_url(path)
        return redirect(signed_url)
    else:
        if path.startswith("~"):
            path = os.path.expanduser(path)
        logger.info(f"Sending file {path}")
        return send_file(path, mimetype=mime_type.get(ext, "application/octet-stream"))


@fs_bp.post("/upload")
@handle_api_errors
def upload_file() -> Response:
    path = require_arg("path")
    try:
        content = request.json["content"] if request.json else None
        if content is None:
            raise KeyError("content")
    except (KeyError, ValueError, AssertionError) as e:
        raise InvalidInputException('Invalid content. Expecting JSON: {"content": "xxx"}') from e

    if path.startswith("s3://"):
        s3_client = current_app.config["S3_CLIENT"]
        try:
            S3FileSystem(s3_client).put_file(path, content)
            return jsonify({"status": "success"})
        except ClientError as e:
            msg = str(e)
            if "AccessDenied" in msg:
                raise AccessDeniedException(msg) from e
            else:
                raise e
    else:
        if path.startswith("~"):
            path = os.path.expanduser(path)
        pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
    return jsonify({"status": "success"})
