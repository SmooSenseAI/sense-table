import logging
from rich.logging import RichHandler


# Configure Rich logger
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

def getLogger(name: str):
    return logging.getLogger(name)