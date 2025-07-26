import logging
from flask import request, jsonify
import duckdb
from timeit import default_timer
from flask import Blueprint, jsonify
from sense_table.utils.serialization import serialize


logger = logging.getLogger(__name__)
query_bp = Blueprint('query', __name__, url_prefix='/api')


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

