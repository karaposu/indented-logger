It seems that the logging output is still showing the `_log_key_value` and `_log_object` function names in the debug messages. This might not be the intended outcome since these function names can clutter the log output and detract from the actual message.

### Solution:
To avoid logging the function names in the output, we should revise the logging calls so that the `extra` dictionary only includes relevant information without showing the function names. Here’s how you can do that:

1. **Remove the function names from the logging messages**: Instead of including the helper function names in the `extra` dictionary, focus only on the necessary context.

Here's how you can modify your logging functions:

```python
import logging
import re
import inspect

def flatten_string(s):
    """
    Flattens the given multi-line string into a single line.
    """
    flattened = re.sub(r'\s+', ' ', s).strip()
    return flattened

def smart_indent_log(logger_object, obj, lvl, exclude=None, name=None, flatten_long_strings=True):
    """
    Logs the contents of an object or dictionary with indentation based on the nesting level.
    """
    if exclude is None:
        exclude = []

    caller_func = inspect.stack()[1].function  # Get the caller function name

    if name:
        logger_object.debug(f"{name}:", extra={"lvl": lvl})  # No longer adding callerFunc here
        lvl += 1

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

    if hasattr(obj, "__dict__"):
        dictionary = obj.__dict__
    elif isinstance(obj, dict):
        dictionary = obj
    else:
        _log_simple_value(logger_object, obj, lvl, flatten_long_strings)
        return

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
```

### Key Changes:
- **Removed the `callerFunc` attribute**: This change eliminates the clutter in the logs by not including the helper function names in the `extra` dictionary.
- **Streamlined `logger_object.debug` calls**: The logging now focuses on the message content without appending function names.

### Result:
After these changes, your log output should show the data neatly without the function references. For example, you should see something like:

```
2024-10-24 16:57:06,152 - DEBUG    -                         Record:                                                   
2024-10-24 16:57:06,152 - DEBUG    -                             ready: True                                            
2024-10-24 16:57:06,152 - DEBUG    -                             record_id: 3                                          
2024-10-24 16:57:06,152 - DEBUG    -                             record: Encard Harcaması, I.-SHOP WWW.PZZ.BY PAR g.p.
...
```

Let me know if this helps or if you have more adjustments in mind!