import os
from sense_table.app import SenseTableApp
from sense_table.settings import SenseTableSettings
from flask import Flask

PWD = os.path.dirname(os.path.abspath(__file__))

app = SenseTableApp(url_prefix='', settings=SenseTableSettings(
    folderBrowserDefaultRootFolder='s3://sense-table-demo',
    licenseKey= "GBQvhcqo1GHk6VBpI0PYsZwfhuQdoYTYHhEHQT8HnExJv8WG_7lCkezzMtIimlSQ1sZrDjqhFAmASYHXIPvsDQ==|6vtGq0Yhb1BXsXOonjSfx_JVaab7kmCU_XSRf7dmjYs=|eyJkb21haW4iOiAicjA5M2JsMW56aC5leGVjdXRlLWFwaS51cy13ZXN0LTIuYW1hem9uYXdzLmNvbSIsICJ1cmxfcHJlZml4IjogIi9kZXYiLCAidmFsaWRfdW50aWwiOiAiMjAyNi0wOC0wNiJ9"
)).create_app()


@app.route('/echo')
def index():
    from flask import request
    url = request.url
    params = '<ul>'
    for param, value in request.args.items():
        params += f'<li>{param}: {value}</li>'
    params += '</ul>'
    headers = '<ul>'
    for header, value in request.headers.items():
        headers += f'<li>{header}: {value}</li>'
    headers += '</ul>'
    
    cookies = '<ul>'
    for cookie, value in request.cookies.items():
        cookies += f'<li>{cookie}: {value}</li>'
    cookies += '</ul>'
    
    return f"""
    <h3>URL:</h3>
    {url}
    <h3>Params:</h3>
    {params}
    <h3>Headers:</h3>
    {headers}
    <h3>Cookies:</h3> 
    {cookies}
    """


if __name__ == '__main__':
    app.run()