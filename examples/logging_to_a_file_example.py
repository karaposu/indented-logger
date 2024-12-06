from indented_logger import setup_logging, log_indent
import logging

# Configure to log both to console and file:
# - Console: With ANSI colors and indentation
# - File: No ANSI colors, no indentation
setup_logging(
    level=logging.INFO,
    log_file='application.log',
    include_func=True,
    log_file_keep_ANSI=False,    # No ANSI in file
    log_file_no_indent=False      # No indentation in file logs
)

logger = logging.getLogger(__name__)

@log_indent
def complex_operation():
    logger.info("Starting complex operation")
    sub_operation()
    logger.info("Complex operation completed")

@log_indent
def sub_operation():
    logger.info("Performing sub operation step 1")
    logger.info("Performing sub operation step 2")

complex_operation()

