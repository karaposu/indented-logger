import logging
from indented_logger import setup_logging

# Configure logging with use_logger_hierarchy enabled
setup_logging(
    level=logging.DEBUG,
    include_func=True,
    include_module=True,
    truncate_messages=False,
    min_func_name_col=120,
    indent_spaces=4
)

# Get the logger for this module
logger = logging.getLogger(__name__)

# Import module1 and call its function
from examples.module1.module1 import module1_function

def main():
    # logger.info('Starting main function',extra={"color": "RED"})

    logger.debug("Starting main function", extra={"lvl": 5, "c": "red"})
    logger.debug("Starting main function", extra={"lvl": 5})
    module1_function()
    logger.info('Finished main function')

if __name__ == '__main__':
    main()







