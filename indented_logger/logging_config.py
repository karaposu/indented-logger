# indented_logger/logging_config.py

import logging
from .formatter import IndentFormatter

def setup_logging(level=logging.DEBUG, log_file=None, include_func=False,
                  truncate_messages=False, min_func_name_col=80):
    # Create the formatter
    formatter = IndentFormatter(
        include_func=include_func,
        truncate_messages=truncate_messages,
        min_func_name_col=min_func_name_col
    )

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Add handlers only if they haven't been added yet
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if a log_file is specified)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    # Optionally disable propagation if you don't want logs to propagate to the root logger in other libraries
    # logger.propagate = False
