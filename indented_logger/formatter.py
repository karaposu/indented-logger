# indented_logger/formatter.py

import logging
from .indent import get_indent_level

class IndentFormatter(logging.Formatter):
    def __init__(self, include_func=False, truncate_messages=False, min_func_name_col=80,
                 use_logger_hierarchy=False, datefmt=None, indent_spaces=4):
        self.include_func = include_func
        self.truncate_messages = truncate_messages
        self.min_func_name_col = min_func_name_col
        self.use_logger_hierarchy = use_logger_hierarchy
        self.indent_spaces = indent_spaces
        if include_func:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s%(padding)s{%(name)s}'
        else:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s'
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        # Thread-local indent from @log_indent decorators
        thread_indent = get_indent_level()

        # Manual indent from 'lvl' parameter
        manual_indent = getattr(record, 'lvl', 0)

        # Hierarchy-based indent from logger name
        if self.use_logger_hierarchy:
            hierarchy_indent = record.name.count('.')
        else:
            hierarchy_indent = 0

        # Total indentation level
        total_indent = thread_indent + manual_indent + hierarchy_indent

        # Generate indentation string
        indent = ' ' * (total_indent * self.indent_spaces)

        # Original message with indentation
        message = f"{indent}{record.getMessage()}"

        # Handle message truncation if enabled
        if self.truncate_messages:
            max_message_length = 50  # You can parameterize this if desired
            if len(message) > max_message_length:
                message = message[:max_message_length - 3] + '...'

        # Build base log line and calculate its length
        asctime = self.formatTime(record, self.datefmt)
        levelname = f"{record.levelname:<8}"
        base_log = f"{asctime} - {levelname} - {message}"

        if self.include_func:
            # Calculate padding to align function names
            base_log_len = len(base_log)
            if base_log_len < self.min_func_name_col:
                spaces_needed = self.min_func_name_col - base_log_len
                padding = ' ' * spaces_needed
            else:
                padding = ' '
            # Update record attributes
            record.padding = padding
        else:
            record.padding = ''

        # Temporarily store the original message and arguments
        original_msg = record.msg
        original_args = record.args
        try:
            # Set the record's message to our formatted message
            record.msg = message
            record.args = ()
            return super().format(record)
        finally:
            # Restore the original message and arguments
            record.msg = original_msg
            record.args = original_args
