# indented_logger/logging_config.py

import logging
from .formatter import IndentFormatter

def setup_logging(level=logging.DEBUG, log_file=None, include_func=False, include_module=False,
                  func_module_format=None, truncate_messages=False, min_func_name_col=120,
                  indent_modules=False, indent_packages=False, indent_spaces=4, datefmt=None,
                  debug=False):
    # Create the formatter with the new parameters
    formatter = IndentFormatter(
        include_func=include_func,
        include_module=include_module,
        func_module_format=func_module_format,
        truncate_messages=truncate_messages,
        min_func_name_col=min_func_name_col,
        indent_modules=indent_modules,
        indent_packages=indent_packages,
        indent_spaces=indent_spaces,
        datefmt=datefmt,
        debug=debug
    )

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Add handlers only if they haven't been added yet
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler (if a log_file is specified)
    if log_file and not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
