import logging
from examples.module1.module2.module2 import module2_function

# Get the logger for this module
logger = logging.getLogger(__name__)

def module1_function():
    logger.info('Entered module1_function')
    module2_function()
    logger.info('Exiting module1_function')
