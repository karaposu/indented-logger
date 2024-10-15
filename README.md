
# indented_logger

**indented_logger** is a custom formatter for Python's standard `logging` package that adds **automatic indentation** and enhanced formatting support. (Without altering original logger class and **not causing any compatibility issues**)

It visually represents the hierarchical structure and depth of your logging messages, making it easier to understand the flow of execution in complex systems. And it  


## Features

- **Automatic Indentation via Decorators**: Use decorators to automatically manage indentation levels based on function call hierarchy.
- **Manual Indentation Support with `lvl`**: Add manual indentation to specific log messages for granular control using the `lvl` parameter.
- **Custom Formatter and Logger**: Includes an `IndentFormatter` that handles indentation and formatting seamlessly.
- **Optional Function Names**: Choose to include or exclude function names in your log messages.
- **Function Name Alignment**: Align function names at a specified column for consistent and readable logs.
- **Message Truncation (Optional)**: Optionally truncate long messages to a specified length.
- **Thread Safety**: Manages indentation levels per thread, ensuring correct behavior in multi-threaded applications.
- **Easy Integration**: Seamlessly integrates with existing logging setups with minimal changes.

## Installation

You can install IndentedLogger via pip:

```bash
pip install indented_logger
```

## Usage

### Basic Setup

```python
from indented_logger import setup_logging
import logging
# Configure the logger
setup_logging(level=logging.INFO, include_func=True)
# Get the logger
logger = logging.getLogger(__name__)
# Basic logging, indented_logger does not cause compatibility issues with normal loggers
logger.info('Starting process A')
# manual indentation
logger.info('Details of process A', extra={'lvl':1})
logger.info('Deeper Details of process A', extra={'lvl':2})
logger.info('Process complete')
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Starting process A                          {main}
2024-08-15 12:34:56 - INFO     -     Details of process A                    {main}
2024-08-15 12:34:58 - INFO     -         Deeper Details of process A         {main}
2024-08-15 12:34:59 - INFO     - Process complete                            {main}
```

### Automatic Indentation with Decorators

Use the `@log_indent` decorator to automatically manage indentation levels based on function calls.

```python
from indented_logger import setup_logging, log_indent
import logging

# Setup the logger with function names included
setup_logging(level=logging.INFO, include_func=True)

logger = logging.getLogger(__name__)

@log_indent
def start_process():
    logger.info('Starting process')
    load_data()
    process_data()
    logger.info('Process complete')

@log_indent
def load_data():
    logger.info('Loading data')

@log_indent
def process_data():
    logger.info('Processing data')

start_process()
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Starting process                            {start_process}
2024-08-15 12:34:56 - INFO     -     Loading data                            {load_data}
2024-08-15 12:34:56 - INFO     -     Processing data                         {process_data}
2024-08-15 12:34:56 - INFO     - Process complete                            {start_process}
```

### Manual Indentation with `lvl`

You can manually adjust indentation levels using the `lvl` parameter in logging calls. The higher the value of `lvl`, the deeper the indentation.

```python
# Manual indentation using `lvl`
logger.info('Starting process', extra={'lvl': 0})
logger.info('Loading data', extra={'lvl': 1})
logger.info('Processing data', extra={'lvl': 2})
logger.info('Saving results', extra={'lvl': 1})
logger.info('Process complete', extra={'lvl': 0})
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Starting process
2024-08-15 12:34:56 - INFO     -     Loading data
2024-08-15 12:34:56 - INFO     -         Processing data
2024-08-15 12:34:56 - INFO     -     Saving results
2024-08-15 12:34:56 - INFO     - Process complete
```

### Including or Excluding Function Names

You can choose to include or exclude function names in your log messages by setting the `include_func` parameter when configuring the logger.

```python
# Include function names
setup_logging(level=logging.INFO, include_func=True)

# Exclude function names
setup_logging(level=logging.INFO, include_func=False)
```

### Aligning Function Names at a Specific Column

You can align function names at a specific column using the `min_func_name_col` parameter. This ensures that the function names start at the same column in each log entry, improving readability.

```python
# Setup the logger with function names included and alignment at column 100
setup_logging(level=logging.INFO, include_func=True, min_func_name_col=100)

logger = logging.getLogger(__name__)

@log_indent
def example_function():
    logger.info('This is a log message that might be quite long and needs proper alignment')

example_function()
```

**Output:**

```
2024-08-15 12:34:56 - INFO     -     This is a log message that might be quite long and needs proper alignment       {example_function}
```

**Explanation:**

- The function names are aligned at or after the 100th character column.
- If the message is longer than the specified column, the function name moves further to the right, ensuring the message is not truncated.

### Message Truncation (Optional)

You can enable message truncation to limit the length of log messages. Set the `truncate_messages` parameter to `True` when configuring the logger.

```python
# Setup the logger with message truncation enabled
setup_logging(level=logging.INFO, include_func=True, truncate_messages=True)

logger = logging.getLogger(__name__)

@log_indent
def example_function():
    logger.info('This is a very long log message that will be truncated to a maximum length')

example_function()
```

**Output:**

```
2024-08-15 12:34:56 - INFO     -     This is a very long log message th...    {example_function}
```

**Notes:**

- The messages are truncated to a default maximum length (e.g., 50 characters).
- You can adjust the maximum message length by modifying the `max_message_length` variable in the `IndentFormatter` class.

## Benefits

- **Enhanced Readability**: Visually represent the hierarchy and depth of operations in your logs.
- **Organized Logs**: Group related log messages, making it easier to understand nested processes.
- **Simplicity**: Minimalistic design adds just what you need without altering core logging functionalities.
- **Customizable Formatting**: Control inclusion of function names, alignment, and message truncation.
- **Easy Integration**: Works with existing logging setups with minimal changes to your configuration.
- **Flexible Indentation**: Supports both automatic and manual indentation for granular control.

## License

IndentedLogger is released under the [MIT License](LICENSE).

---

*Note: If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.*

---

## Additional Details

### IndentedLogger Parameters for `setup_logging`

- `level` (int): Logging level (e.g., `logging.INFO`, `logging.DEBUG`).
- `include_func` (bool, optional): Whether to include function names in log messages. Default is `False`.
- `truncate_messages` (bool, optional): Whether to truncate long messages. Default is `False`.
- `min_func_name_col` (int, optional): The minimum column at which function names should appear. Default is `80`.

### Example with All Parameters

```python
setup_logging(
    level=logging.DEBUG,
    include_func=True,
    truncate_messages=False,
    min_func_name_col=100
)
```

### Customizing Indentation and Formatting

- **Adjust Indentation Width**: Modify the number of spaces used for each indentation level by changing the multiplication factor in the `IndentFormatter` class.
- **Set Date Format**: Pass a `datefmt` parameter when configuring `setup_logging` or `IndentFormatter` to customize the timestamp format.

### Thread Safety

IndentedLogger uses thread-local storage to manage indentation levels per thread, ensuring that logs from different threads are correctly indented.

### Advanced Usage

For advanced use cases, you can extend or modify the `IndentFormatter` class to suit your specific requirements.

---


