import logging
from flask import request, jsonify, send_file, current_app
from flask import Blueprint, jsonify
import os
import subprocess

logger = logging.getLogger(__name__)
fs_bp = Blueprint('fs', __name__)


@fs_bp.get('/ls')
def get_ls():
    path = request.args.get('path')
    limit = int(request.args.get('limit', 100))
    show_hidden = request.args.get('show_hidden', 'false').lower() == 'true'
    if path.startswith('~'):
        path = os.path.expanduser(path)
    if not os.path.exists(path):
        return jsonify({"error": f"Path {path} does not exist"}), 404
        
    items = []
    try:
        for entry in os.scandir(path):
            if entry.name.startswith('.') and not show_hidden:
                continue
            items.append({
                "name": entry.name,
                "size": entry.stat().st_size,
                "lastModified": int(1000 * entry.stat().st_mtime),
                "isDir": entry.is_dir(),
            })
            if len(items) >= limit:
                break
           
    except PermissionError:
        return jsonify({"error": f"Permission denied accessing {path}"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(items)

@fs_bp.get('/get-file')
def get_file():
    path = request.args.get('path')
    if path.startswith('~'):
        path = os.path.expanduser(path)
    if not os.path.exists(path):
        return jsonify({"error": f"Path {path} does not exist"}), 404
    ext = os.path.splitext(path)[1]
    mime_type = {
        '.json': 'application/json',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
    }
    return send_file(path, mimetype=mime_type.get(ext, 'application/octet-stream'))


@fs_bp.post('/bash')
def run_bash():
    command = request.json['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return jsonify({
        'status': 'success',
        'output': result.stdout,
        'error': result.stderr,
    })