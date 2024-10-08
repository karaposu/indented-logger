# indented_logger/decorator.py

import functools
from .indent import increase_indent, decrease_indent

def log_indent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        increase_indent()
        try:
            return func(*args, **kwargs)
        finally:
            decrease_indent()
    return wrapper
