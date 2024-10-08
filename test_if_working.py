import logging
from indented_logger import setup_logging, log_indent

# Configure logging
setup_logging(
    level=logging.DEBUG,
    include_func=True,
    truncate_messages=False,
    min_func_name_col=100
)

logger = logging.getLogger(__name__)

# @log_indent
def my_function():
    logger.info('This is an indented log message', extra={"lvl":4})

my_function()
