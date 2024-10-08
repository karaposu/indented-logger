# indented_logger/indent.py

import threading

# Thread-local storage for indentation levels
_thread_local = threading.local()

def get_indent_level():
    return getattr(_thread_local, 'indent_level', 0)

def increase_indent():
    _thread_local.indent_level = get_indent_level() + 1

def decrease_indent():
    current = get_indent_level()
    _thread_local.indent_level = max(current - 1, 0)
