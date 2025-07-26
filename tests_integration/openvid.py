import os
from sense_table.app import SenseTableApp

PWD = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(os.path.dirname(PWD), 'data', 'OpenVid-celebv.parquet')

app = SenseTableApp().create_app()

@app.route('/your-other-page')
def your_other_page():
    return 'hello world'

def start():
    app.run(port=8000)

if __name__ == '__main__':
    start()
    