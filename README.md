# IndentedLogger

IndentedLogger is a powerful yet simple wrapper around Python's standard `logging` package that adds automatic indentation and enhanced formatting support to your logs. It visually represents the hierarchical structure and depth of your logging messages, making it easier to understand the flow of execution in complex systems.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Setup](#basic-setup)
  - [Automatic Indentation with Decorators](#automatic-indentation-with-decorators)
  - [Manual Indentation](#manual-indentation)
  - [Including or Excluding Function Names](#including-or-excluding-function-names)
  - [Aligning Function Names at a Specific Column](#aligning-function-names-at-a-specific-column)
  - [Message Truncation (Optional)](#message-truncation-optional)
- [Benefits](#benefits)
- [License](#license)

## Features

- **Automatic Indentation via Decorators**: Use decorators to automatically manage indentation levels based on function call hierarchy.
- **Manual Indentation Support**: Add manual indentation to specific log messages for granular control.
- **Custom Formatter and Logger**: Includes an `IndentFormatter` and a custom logger class that handle indentation and formatting seamlessly.
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

*Note: Ensure that your Python version is **3.8** or higher to utilize all features effectively.*

## Usage

### Basic Setup

```python
from indented_logger import IndentedLogger
import logging

# Setup the logger
logger_setup = IndentedLogger(name='my_logger', level=logging.INFO)
logger = logger_setup.get_logger()

# Basic logging
logger.info('Starting process')
logger.info('Process complete')
```

### Automatic Indentation with Decorators

Use the `@log_indent` decorator to automatically manage indentation levels based on function calls.

```python
from indented_logger import IndentedLogger, log_indent
import logging

# Setup the logger with function names included
logger_setup = IndentedLogger(name='my_logger', level=logging.INFO, include_func=True)
logger = logger_setup.get_logger()

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
2024-08-15 12:34:56 - INFO     - Entering function: start_process           {start_process}
2024-08-15 12:34:56 - INFO     -     Starting process                       {start_process}
2024-08-15 12:34:56 - INFO     -     Entering function: load_data           {load_data}
2024-08-15 12:34:56 - INFO     -         Loading data                       {load_data}
2024-08-15 12:34:56 - INFO     -     Exiting function: load_data            {load_data}
2024-08-15 12:34:56 - INFO     -     Entering function: process_data        {process_data}
2024-08-15 12:34:56 - INFO     -         Processing data                    {process_data}
2024-08-15 12:34:56 - INFO     -     Exiting function: process_data         {process_data}
2024-08-15 12:34:56 - INFO     -     Process complete                       {start_process}
2024-08-15 12:34:56 - INFO     - Exiting function: start_process            {start_process}
```

### Manual Indentation

You can manually adjust indentation levels using the `lvl` parameter in logging calls.

```python
# Manual indentation
logger.info('Starting process', lvl=0)
logger.info('Loading data', lvl=1)
logger.info('Processing data', lvl=2)
logger.info('Saving results', lvl=1)
logger.info('Process complete', lvl=0)
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

Include or exclude function names in your log messages by setting the `include_func` parameter when initializing `IndentedLogger`.

```python
# Include function names
logger_setup = IndentedLogger(name='my_logger', level=logging.INFO, include_func=True)

# Exclude function names
logger_setup = IndentedLogger(name='my_logger', level=logging.INFO, include_func=False)
```

### Aligning Function Names at a Specific Column

You can align function names at a specific column using the `min_func_name_col` parameter. This ensures that the function names start at the same column in each log entry, improving readability.

```python
# Setup the logger with function names included and alignment at column 80
logger_setup = IndentedLogger(
    name='my_logger',
    level=logging.INFO,
    include_func=True,
    min_func_name_col=80
)
logger = logger_setup.get_logger()

@log_indent
def example_function():
    logger.info('This is a log message that might be quite long and needs proper alignment')

example_function()
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Entering function: example_function                      {example_function}
2024-08-15 12:34:56 - INFO     -     This is a log message that might be quite long and needs proper alignment  {example_function}
2024-08-15 12:34:56 - INFO     - Exiting function: example_function                       {example_function}
```

**Explanation:**

- The function names are aligned at or after the 80th character column.
- If the message is longer than the specified column, the function name moves further to the right, ensuring the message is not truncated.

### Message Truncation (Optional)

You can enable message truncation to limit the length of log messages. Set the `truncate_messages` parameter to `True` when initializing `IndentedLogger`.

```python
# Setup the logger with message truncation enabled
logger_setup = IndentedLogger(
    name='my_logger',
    level=logging.INFO,
    include_func=True,
    truncate_messages=True
)
logger = logger_setup.get_logger()

@log_indent
def example_function():
    logger.info('This is a very long log message that will be truncated to a maximum length')

example_function()
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Entering function: example_function      {example_function}
2024-08-15 12:34:56 - INFO     -     This is a very long log message th...{example_function}
2024-08-15 12:34:56 - INFO     - Exiting function: example_function       {example_function}
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

### IndentedLogger Class Parameters

- `name` (str): The name of the logger.
- `level` (int): Logging level (e.g., `logging.INFO`, `logging.DEBUG`).
- `log_file` (str, optional): Path to a log file. If provided, logs will also be written to this file.
- `include_func` (bool, optional): Whether to include function names in log messages. Default is `False`.
- `truncate_messages` (bool, optional): Whether to truncate long messages. Default is `False`.
- `min_func_name_col` (int, optional): The minimum column at which function names should appear. Default is `80`.

### Example with All Parameters

```python
logger_setup = IndentedLogger(
    name='my_logger',
    level=logging.DEBUG,
    log_file='app.log',
    include_func=True,
    truncate_messages=False,
    min_func_name_col=80
)
logger = logger_setup.get_logger()
```

### Customizing Indentation and Formatting

- **Adjust Indentation Width**: Modify the number of spaces used for each indentation level by changing the multiplication factor in the `IndentFormatter` class.
- **Set Date Format**: Pass a `datefmt` parameter when initializing `IndentedLogger` or `IndentFormatter` to customize the timestamp format.

### Thread Safety

IndentedLogger uses thread-local storage to manage indentation levels per thread, ensuring that logs from different threads are correctly indented.

### Advanced Usage

For advanced use cases, you can extend or modify the `CustomLogger` and `IndentFormatter` classes to suit your specific requirements.

---

*This updated documentation reflects the latest features and enhancements made to IndentedLogger, providing you with greater control and flexibility over your logging output.*