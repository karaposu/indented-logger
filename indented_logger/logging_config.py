# indented_logger/logging_config.py

import logging
from .formatter import IndentFormatter

def setup_logging(level=logging.DEBUG,
                  log_file=None,
                  include_func=False,
                  include_module=False,
                  func_module_format=None,
                  truncate_messages=False,
                  min_func_name_col=120,
                  indent_modules=False,
                  indent_packages=False,
                  indent_spaces=4,
                  datefmt=None,
                  debug=False,
                  log_file_keep_ANSI=False,
                  log_file_no_indent=False, 
                  no_datetime=False):
    """
    Set up logging with indentation and optional file output.

    Parameters
    ----------
    level : int
        Logging level (e.g., `logging.INFO`, `logging.DEBUG`).
    log_file : str or None
        Path to a file for saving logs. If None, no file logging is performed.
    include_func : bool
        Include function names in the log output.
    include_module : bool
        Include module names in the log output.
    func_module_format : str or None
        Format string for {funcName} and {moduleName}.
    truncate_messages : bool
        If True, truncate long messages to a fixed length.
    min_func_name_col : int
        The column at which function/module names should start.
    indent_modules : bool
        If True, automatically indent logs based on whether they come from a module other than __main__.
    indent_packages : bool
        If True, automatically indent logs based on the depth of the package hierarchy.
    indent_spaces : int
        Number of spaces per indentation level.
    datefmt : str or None
        Date format for the log timestamps.
    debug : bool
        If True, enable debug mode in the formatter.
    log_file_keep_ANSI : bool
        If False, remove ANSI color codes from file logs. Defaults to False.
    log_file_no_indent : bool
        If True, no indentation logic is applied to file logs. Defaults to False.

    Returns
    -------
    None
    """
    # Console formatter with colors and indentation
    console_formatter = IndentFormatter(
        include_func=include_func,
        include_module=include_module,
        func_module_format=func_module_format,
        truncate_messages=truncate_messages,
        min_func_name_col=min_func_name_col,
        indent_modules=indent_modules,
        indent_packages=indent_packages,
        indent_spaces=indent_spaces,
        datefmt=datefmt,
        debug=debug,
        disable_colors=False,
        disable_indent=False,
        no_datetime=no_datetime
    )

    # File formatter with optional removal of ANSI and indentation
    # We'll add two new parameters to IndentFormatter for internal logic:
    # - disable_colors (bool): If True, strip ANSI codes
    # - disable_indent (bool): If True, no indentation logic applied
    file_formatter = IndentFormatter(
        include_func=include_func,
        include_module=include_module,
        func_module_format=func_module_format,
        truncate_messages=truncate_messages,
        min_func_name_col=min_func_name_col,
        indent_modules=(False if log_file_no_indent else indent_modules),
        indent_packages=(False if log_file_no_indent else indent_packages),
        indent_spaces=(0 if log_file_no_indent else indent_spaces),
        datefmt=datefmt,
        debug=debug,
        disable_colors=(not log_file_keep_ANSI),
        disable_indent=log_file_no_indent,
        no_datetime=no_datetime
    )

    logger = logging.getLogger()
    logger.setLevel(level)

    # Add console handler if none present
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Add file handler if log_file specified and not already present
    if log_file and not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
