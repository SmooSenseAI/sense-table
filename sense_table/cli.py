import click
import os
from sense_table.app import SenseTableApp
from sense_table.settings import SenseTableSettings

@click.command()
@click.option('--port', default=8000, type=int)
def main(port):
    settings = SenseTableSettings(
        folderBrowserDefaultRootFolder=os.getcwd()
    )

    SenseTableApp(settings=settings).run(port=port)

if __name__ == '__main__':
    main()