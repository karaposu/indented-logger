# indented_logger/formatter.py

import logging
import re
from .indent import get_indent_level

class IndentFormatter(logging.Formatter):
    COLOR_MAP = {
        "red": '\033[31m',
        "green": '\033[32m',
        "yellow": '\033[33m',
        "blue": '\033[34m',
        "magenta": '\033[35m',
        "cyan": '\033[36m',
        "reset": '\033[0m'
    }

    def __init__(self, include_func=False, include_module=False, func_module_format=None,
                 truncate_messages=False, min_func_name_col=120, indent_modules=False,
                 indent_packages=False, datefmt=None, indent_spaces=4, debug=False,
                 disable_colors=False, disable_indent=False):
        self.include_func = include_func
        self.include_module = include_module
        self.truncate_messages = truncate_messages
        self.min_func_name_col = min_func_name_col
        self.indent_modules = indent_modules and not disable_indent
        self.indent_packages = indent_packages and not disable_indent
        self.indent_spaces = 0 if disable_indent else indent_spaces
        self.debug = debug
        self.disable_colors = disable_colors
        self.disable_indent = disable_indent

        self.func_module_format = self.build_func_module_format(func_module_format)

        fmt = '%(asctime)s - %(levelname)-8s - %(message)s'
        if self.func_module_format:
            fmt += '%(padding)s{%(func_module_info)s}'

        super().__init__(fmt=fmt, datefmt=datefmt)

    def build_func_module_format(self, func_module_format):
        if func_module_format is None:
            placeholders = []
            if self.include_module:
                placeholders.append('{moduleName}')
            if self.include_func:
                placeholders.append('{funcName}')
            return ':'.join(placeholders) if placeholders else ''
        return func_module_format

    def get_indent(self, record):
        if self.disable_indent:
            # No indentation logic applied
            return ''
        thread_indent = get_indent_level()
        manual_indent = getattr(record, 'lvl', 0)
        hierarchy_indent = 0
        if self.indent_modules and record.name != '__main__':
            hierarchy_indent += 1
        if self.indent_packages:
            hierarchy_indent += record.name.count('.')

        total_indent = thread_indent + manual_indent + hierarchy_indent
        return ' ' * (total_indent * self.indent_spaces)

    def strip_color_codes(self, text):
        return re.sub(r'\033\[\d+m', '', text)

    def apply_colors(self, text, color_name='reset'):
        if self.disable_colors:
            return text
        color = self.COLOR_MAP.get(color_name.lower(), self.COLOR_MAP['reset'])
        return f"{color}{text}{self.COLOR_MAP['reset']}"

    def get_colored_message(self, record, indent):
        color_name = getattr(record, 'c', 'reset').lower()
        message = f"{indent}{record.getMessage()}"

        if self.truncate_messages:
            max_message_length = 50
            if len(message) > max_message_length:
                message = message[:max_message_length - 3] + '...'

        if self.disable_colors:
            # Just return the plain message if colors are disabled
            return message
        else:
            return self.apply_colors(message, color_name)

    def get_func_module_info(self, record):
        if self.func_module_format:
            return self.func_module_format.format(funcName=record.funcName, moduleName=record.name)
        return ''

    def apply_padding(self, asctime, levelname, message, func_module_info):
        stripped_message = self.strip_color_codes(message) if not self.disable_colors else message
        current_length = len(asctime) + 3 + len(levelname) + 3 + len(stripped_message)
        desired_column = self.min_func_name_col

        return ' ' * max(0, desired_column - current_length) if func_module_info else ''

    def format(self, record):
        indent = self.get_indent(record)
        message = self.get_colored_message(record, indent)

        asctime = self.formatTime(record, self.datefmt)
        asctime_colored = self.apply_colors(asctime, 'cyan') if not self.disable_colors else asctime

        levelname = f"{record.levelname:<8}"
        func_module_info = self.get_func_module_info(record)

        padding = self.apply_padding(asctime, levelname, message, func_module_info)

        original_msg, original_args = record.msg, record.args
        try:
            record.msg = message
            record.args = ()
            record.func_module_info = func_module_info
            record.padding = padding

            formatted_message = super().format(record)

            if self.usesTime() and not self.disable_colors:
                formatted_message = formatted_message.replace(asctime, asctime_colored, 1)

            return formatted_message
        finally:
            record.msg, record.args = original_msg, original_args
