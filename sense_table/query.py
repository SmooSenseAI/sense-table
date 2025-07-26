import logging
from flask import request, jsonify
import math
import duckdb
from timeit import default_timer
from flask import Blueprint, jsonify



logger = logging.getLogger(__name__)
query_bp = Blueprint('query', __name__, url_prefix='/api')


def serialize(obj):
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    elif isinstance(obj, (list, tuple, set)):
        return [serialize(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, bytes):
        return f'{obj.hex()}'
    return obj


@query_bp.post('/query')
def query():
    time_start = default_timer()
    query = request.json['query']
    con = duckdb.connect()
    column_names = []
    rows = []
    error = None
    try:
        result = con.execute(query)
        column_names = [desc[0] for desc in result.description]
        rows = result.fetchall()
   
    except Exception as e:
        error = str(e)
    
    return jsonify({
            'status': 'success' if not error else 'error',
            'column_names': column_names,
            'rows': serialize(rows),
            'runtime': default_timer() - time_start,
            'error': error,
        })

