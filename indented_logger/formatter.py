# indented_logger/formatter.py

import logging
from .indent import get_indent_level

class IndentFormatter(logging.Formatter):
    def __init__(self, include_func=False, include_module=False, func_module_format=None,
                 truncate_messages=False, min_func_name_col=120, indent_modules=False,
                 indent_packages=False, datefmt=None, indent_spaces=4, debug=False):
        self.include_func = include_func
        self.include_module = include_module
        self.truncate_messages = truncate_messages
        self.min_func_name_col = min_func_name_col
        self.indent_modules = indent_modules
        self.indent_packages = indent_packages
        self.indent_spaces = indent_spaces
        self.debug = debug  # Debug flag

        # Dynamically build the func_module_format based on include flags
        if func_module_format is None:
            # Default format based on inclusion flags
            placeholders = []
            if self.include_module:
                placeholders.append('{moduleName}')
            if self.include_func:
                placeholders.append('{funcName}')
            if placeholders:
                self.func_module_format = ':'.join(placeholders)
            else:
                self.func_module_format = ''
        else:
            # Use the provided func_module_format
            self.func_module_format = func_module_format

        # Build the format string dynamically
        if self.func_module_format:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s%(padding)s{%(func_module_info)s}'
        else:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s'

        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        # Thread-local indent from @log_indent decorators
        thread_indent = get_indent_level()

        # Manual indent from 'lvl' parameter
        manual_indent = getattr(record, 'lvl', 0)

        # Indentation based on module and package hierarchy
        hierarchy_indent = 0
        if self.indent_modules and record.name != '__main__':
            hierarchy_indent += 1
        if self.indent_packages:
            hierarchy_indent += record.name.count('.')

        # Total indentation level
        total_indent = thread_indent + manual_indent + hierarchy_indent

        # Generate indentation string
        indent = ' ' * (total_indent * self.indent_spaces)

        # Original message with indentation
        message = f"{indent}{record.getMessage()}"

        # Handle message truncation if enabled
        if self.truncate_messages:
            max_message_length = 50  # Parameterize if desired
            if len(message) > max_message_length:
                message = message[:max_message_length - 3] + '...'

        # Prepare variables for formatting
        asctime = self.formatTime(record, self.datefmt)
        levelname = f"{record.levelname:<8}"

        # Add coloring to asctime
        asctime_colored = f"{BLUE}{asctime}{RESET}"

        # Add debug statements if debug mode is enabled
        if self.debug:
            print("DEBUG: record.name =", record.name)
            print("DEBUG: record.funcName =", record.funcName)
            print("DEBUG: func_module_format =", self.func_module_format)

        # Build the func_module_info string based on the format provided
        if self.func_module_format:
            func_module_info = self.func_module_format.format(
                funcName=record.funcName,
                moduleName=record.name
            )
            if self.debug:
                print("DEBUG: func_module_info =", func_module_info)

            record.func_module_info = func_module_info

            # Calculate padding to align func_module_info at min_func_name_col
            desired_column = self.min_func_name_col
            # Calculate the length of the log line up to the message (excluding func_module_info)
            current_length = len(asctime) + 3 + len(levelname) + 3 + len(message)

            if current_length < desired_column:
                spaces_needed = desired_column - current_length
                padding = ' ' * spaces_needed
            else:
                padding = ' '
            record.padding = padding
        else:
            record.padding = ''
            record.func_module_info = ''

        # Temporarily store the original message and arguments
        original_msg = record.msg
        original_args = record.args
        try:
            # Set the record's message to our formatted message
            record.msg = message
            record.args = ()

            # Format the message using the parent class
            formatted_message = super().format(record)

            # Now replace the asctime with the colored asctime
            if self.usesTime():
                formatted_message = formatted_message.replace(asctime, asctime_colored, 1)

            return formatted_message
        finally:
            # Restore the original message and arguments
            record.msg = original_msg
            record.args = original_args


# Define ANSI color codes
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'

# Use in your formatter
class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, RESET)
        message = super().format(record)
        return f"{color}{message}{RESET}"
