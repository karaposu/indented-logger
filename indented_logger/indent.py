# indented_logger/indent.py

import threading

# Thread-local storage for indentation levels
_thread_local = threading.local()

def get_indent_level():
    if not hasattr(_thread_local, 'indent_level'):
        _thread_local.indent_level = 0
    return _thread_local.indent_level

def increase_indent():
    _thread_local.indent_level = get_indent_level() + 1

def decrease_indent():
    current = get_indent_level()
    _thread_local.indent_level = max(current - 1, 0)
