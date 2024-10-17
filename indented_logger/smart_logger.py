def smart_indent_log(logger_object, obj, lvl, exclude=None, name=None):
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
                logger_object.debug(f"{key}: %s", value, extra={"lvl": lvl})
