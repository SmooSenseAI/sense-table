# Installation

SenseTable provides CLI, Python package and MacOS app (coming). You can choose any one that you prefer.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) (an extremely fast Python package manager):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Option 1: CLI


Start a new terminal. Now you can install or update SenseTable:
```bash
uv tool install -U sense-table
```

To run SenseTable, go to the folder containing your data files and simply run command:
```bash
sense

# 👉 Open in your web browser: http://localhost:8000
```

## Option 2: Python package
Python SDK is useful when you want to add your customization or integrate with your other web apps.

It is suggested to do it in a virtual environment to install the package:

```bash
pip install sense-table
```

After installation, start SenseTable:

```py
from sense_table.app import SenseTableApp

app = SenseTableApp().create_app()

@app.route('/your-other-page')
def your_other_page():
    return 'hello world'

def start():
    app.run(port=8000)

if __name__ == '__main__':
    start()
```
