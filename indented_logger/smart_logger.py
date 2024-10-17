import re

def flatten_string(s):
    """
    Flattens the given multi-line string into a single line.

    Parameters:
    s (str): The multi-line string to flatten.

    Returns:
    str: A single-line string with all whitespace compressed.
    """
    # Replace all sequences of whitespace characters with a single space
    flattened = re.sub(r'\s+', ' ', s).strip()
    return flattened

def smart_indent_log(logger_object, obj, lvl, exclude=None, name=None, flatten_long_strings=True):
    """
    Logs the contents of an object or dictionary with indentation based on the nesting level.

    Parameters:
    - logger_object: The logger to use for logging.
    - obj: The object or dictionary to log.
    - lvl: The current indentation level.
    - exclude: A list of keys to exclude from logging.
    - name: An optional name to log before the object's contents.
    - flatten_long_strings: Whether to flatten long strings.
    """
    if exclude is None:
        exclude = []

    if name:
        logger_object.debug(f"{name}:", extra={"lvl": lvl})
        lvl = lvl + 1


    _log_object(logger_object, obj, lvl, exclude, flatten_long_strings)


def _log_object(logger_object, obj, lvl, exclude, flatten_long_strings, _visited=None):
    """
    Helper function to log an object or dictionary.
    """
    if _visited is None:
        _visited = set()

    obj_id = id(obj)
    if obj_id in _visited:
        logger_object.debug("<Recursion detected>", extra={"lvl": lvl})
        return
    _visited.add(obj_id)

    # Check if the object has a __dict__ attribute (e.g., a dataclass or custom class instance)
    if hasattr(obj, "__dict__"):
        dictionary = obj.__dict__
    elif isinstance(obj, dict):
        dictionary = obj
    else:
        # For non-dictionary objects, log their string representation
        _log_simple_value(logger_object, obj, lvl, flatten_long_strings)
        return

    # Log the key-value pairs in the dictionary, excluding specified keys
    for key, value in dictionary.items():
        if key in exclude:
            continue

        if isinstance(value, dict):
            logger_object.debug(f"{key}:", extra={"lvl": lvl})
            _log_object(logger_object, value, lvl + 1, exclude, flatten_long_strings, _visited)
        elif isinstance(value, list):
            logger_object.debug(f"{key}: List of length {len(value)}", extra={"lvl": lvl})
            _log_list(logger_object, value, lvl + 1, exclude, flatten_long_strings, _visited)
        else:
            _log_key_value(logger_object, key, value, lvl, flatten_long_strings)


def _log_list(logger_object, lst, lvl, exclude, flatten_long_strings, _visited):
    """
    Helper function to log a list.
    """
    for index, item in enumerate(lst):
        if isinstance(item, (dict, list)):
            logger_object.debug(f"[{index}]:", extra={"lvl": lvl})
            if isinstance(item, dict):
                _log_object(logger_object, item, lvl + 1, exclude, flatten_long_strings, _visited)
            elif isinstance(item, list):
                _log_list(logger_object, item, lvl + 1, exclude, flatten_long_strings, _visited)
        else:
            _log_simple_value(logger_object, item, lvl, flatten_long_strings, prefix=f"[{index}]")


def _log_key_value(logger_object, key, value, lvl, flatten_long_strings):
    """
    Helper function to log a key-value pair.
    """
    if flatten_long_strings and isinstance(value, str) and len(value) > 120:
        value = flatten_string(value)
    logger_object.debug(f"{key}: {value}", extra={"lvl": lvl})


def _log_simple_value(logger_object, value, lvl, flatten_long_strings, prefix=""):
    """
    Helper function to log a simple value.
    """
    if flatten_long_strings and isinstance(value, str) and len(value) > 120:
        value = flatten_string(value)
    message = f"{prefix}: {value}" if prefix else f"{value}"
    logger_object.debug(message, extra={"lvl": lvl})



