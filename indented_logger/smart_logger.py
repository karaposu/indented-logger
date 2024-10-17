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
    # Ensure 'exclude' is a list to avoid errors
    if exclude is None:
        exclude = []

    # Check if the object has a __dict__ attribute (e.g., a dataclass or custom class instance)
    if hasattr(obj, "__dict__"):
        dictionary = obj.__dict__
    else:
        dictionary = obj  # Assume it's a regular dictionary

    # Log the name if provided
    if name:
        logger_object.debug(f"{name}:", extra={"lvl": lvl})

    # Log the key-value pairs in the dictionary, excluding specified keys
    for key, value in dictionary.items():
        if key not in exclude:
            if isinstance(value, list):
                logger_object.debug(
                    f"{key}: List of length %s", len(value), extra={"lvl": lvl}
                )
            else:
                # Flatten the string if conditions are met
                if flatten_long_strings and isinstance(value, str) and len(value) > 120:
                    value = flatten_string(value)
                logger_object.debug(f"{key}: %s", value, extra={"lvl": lvl})
