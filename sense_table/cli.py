import os
import socket
import threading
import time
import webbrowser
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

import click

from sense_table.app import SenseTableApp
from sense_table.settings import SenseTableSettings

ASCII_ART = """
███████╗███████╗███╗   ██╗███████╗███████╗████████╗ █████╗ ██████╗ ██╗     ███████╗
██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
███████╗█████╗  ██╔██╗ ██║███████╗█████╗     ██║   ███████║██████╔╝██║     █████╗
╚════██║██╔══╝  ██║╚██╗██║╚════██║██╔══╝     ██║   ██╔══██║██╔══██╗██║     ██╔══╝
███████║███████╗██║ ╚████║███████║███████╗   ██║   ██║  ██║██████╔╝███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝
"""


def get_package_version() -> str:
    """Get the installed package version."""
    try:
        return get_version("sense-table")
    except PackageNotFoundError:
        return "dev"


def find_available_port(start_port: int = 8000, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue
    raise RuntimeError(
        f"Could not find an available port in range {start_port}-{start_port + max_attempts - 1}"
    )


def open_browser_after_delay(url: str, delay: int = 1) -> None:
    """Open the default browser after a delay to allow Flask to start."""
    time.sleep(delay)
    webbrowser.open(url)


def run_app() -> None:
    default_folder = os.getcwd()
    port = find_available_port()
    url = f"http://localhost:{port}"

    settings = SenseTableSettings(folderBrowserDefaultRootFolder=default_folder)  # type: ignore
    # Using ANSI escape codes for colors
    print("\033[36m" + ASCII_ART + "\033[0m")  # Cyan color for ASCII art
    print(
        f"\033[32m👉 👉 👉 Open in your web browser: \033[1;34m{url}\033[0m\n\n"
    )  # Green text, blue URL

    # Start browser opening in a separate thread
    browser_thread = threading.Thread(target=open_browser_after_delay, args=(url,), daemon=True)
    browser_thread.start()

    SenseTableApp(settings=settings).run(host="localhost", port=port)


@click.command()
@click.option("--version", "-v", is_flag=True, help="Show the version and exit.")
def main(version: bool) -> None:
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
    run_app()


if __name__ == "__main__":
    main()
