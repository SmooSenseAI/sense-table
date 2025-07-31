import logging
from flask import request, jsonify, current_app
from timeit import default_timer
from flask import Blueprint, jsonify
from sense_table.utils.serialization import serialize
from sense_table.utils.duckdb_connections import check_permissions

logger = logging.getLogger(__name__)
query_bp = Blueprint('query', __name__)


@query_bp.post('/query')
def query():
    connection_maker = current_app.config['DUCKDB_CONNECTION_MAKER']
    con = connection_maker()

    time_start = default_timer()

    query = request.json['query']
    try:
        check_permissions(query)
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    
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

