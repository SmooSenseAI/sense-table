import os
from glob import glob
import collections
import pandas as pd
import duckdb
import shutil
from sense_table.app import SenseTableApp

PWD = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(os.path.dirname(PWD), 'data', 'OpenVid-celebv.parquet')

app = SenseTableApp().create_app()

def start():
    app.run(host='0.0.0.0', port=8000, debug=True)



if __name__ == '__main__':
    start()
    