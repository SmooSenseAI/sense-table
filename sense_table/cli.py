import click
import os
from sense_table.app import SenseTableApp
from sense_table.settings import SenseTableSettings
import textwrap
from importlib.metadata import version, PackageNotFoundError

ASCII_ART = """
███████╗███████╗███╗   ██╗███████╗███████╗████████╗ █████╗ ██████╗ ██╗     ███████╗
██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
███████╗█████╗  ██╔██╗ ██║███████╗█████╗     ██║   ███████║██████╔╝██║     █████╗  
╚════██║██╔══╝  ██║╚██╗██║╚════██║██╔══╝     ██║   ██╔══██║██╔══██╗██║     ██╔══╝  
███████║███████╗██║ ╚████║███████║███████╗   ██║   ██║  ██║██████╔╝███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝
"""

def get_package_version():
    """Get the installed package version."""
    try:
        return version("sense-table")
    except PackageNotFoundError:
        return "development"

@click.command()
@click.option('--port', default=8000, type=int, help='Port to run the server on')
@click.option('--version', '-v', is_flag=True, help='Show the version and exit.')
def main(port, version):
    """Smoothly make sense of your large-scale multi-modal tabular data.
    
    SenseTable provides a web interface for exploring and analyzing your data files.
    Supports CSV, Parquet, and other formats with SQL querying capabilities.
    
    \b
    Examples:
        sense                    # Start SenseTable in current directory
        sense --port 8080        # Use custom port
        sense --version          # Show version information
    """
    
    if version:
        click.echo(f"sense-table, version {get_package_version()}")
        return
    
    default_folder = os.getcwd()
        
    settings = SenseTableSettings(
        folderBrowserDefaultRootFolder=default_folder
    )
    # Using ANSI escape codes for colors
    print("\033[36m" + ASCII_ART + "\033[0m")  # Cyan color for ASCII art
    print(f"\033[32m👉 👉 👉 Open in your web browser: \033[1;34mhttp://localhost:{port}\033[0m\n\n")  # Green text, blue URL
    SenseTableApp(settings=settings).run(host='localhost', port=port)

if __name__ == '__main__':
    main()