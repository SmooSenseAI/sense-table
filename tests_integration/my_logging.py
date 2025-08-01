import logging
from rich.logging import RichHandler


class CommaFormatter(logging.Formatter):
    """Custom formatter that adds commas to relativeCreated time"""
    
    def format(self, record):
        # Format relativeCreated with commas
        record.relativeCreatedFormatted = f"{int(record.relativeCreated):,}"
        return super().format(record)


# Configure Rich logger with custom formatter
handler = RichHandler(rich_tracebacks=True)
handler.setFormatter(CommaFormatter("[%(relativeCreatedFormatted)sms] %(filename)s:%(lineno)d - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

def getLogger(name: str):
    return logging.getLogger(name)