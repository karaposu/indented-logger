# What is IndentedLogger?

**IndentedLogger** is a very simple wrapper around Python's standard logging package that adds indentation support to your logs. It allows you to visually represent the hierarchical structure or depth of your logging messages, making it easier to understand the flow of execution in complex systems.

## Usage and Output 

To get output like this :
```python
2024-08-15 12:34:56 - INFO - Starting process
2024-08-15 12:34:56 - INFO -     Loading data
2024-08-15 12:34:56 - INFO -         Processing data
2024-08-15 12:34:56 - INFO -     Saving results
2024-08-15 12:34:56 - INFO - Process complete

```

```python
from IndentedLogger.indented_logger import IndentedLogger

# Setup the logger
logger_setup = IndentedLogger(name='my_logger', level=logging.INFO, log_file='app.log')
logger = logger_setup.get_logger()

# Log messages with different indentation levels
logger.info('Starting process', extra={'lvl': 0})
logger.info('Loading data', extra={'lvl': 1})
logger.info('Processing data', extra={'lvl': 2})
logger.info('Saving results', extra={'lvl': 1})
logger.info('Process complete', extra={'lvl': 0})

```


IndentedLogger is a lightweight, easy-to-use wrapper for Python's built-in logging module. By extending the usual logging capabilities, it introduces indentation levels to your log messages without adding unnecessary complexity. This small enhancement helps you organize and visualize the structure of your log output, making debugging and process tracking more intuitive.

## Benefits of Using IndentedLogger

- **Simplicity**: It’s a minimalistic wrapper that adds just what you need—indentation—without altering the core logging functionalities you're familiar with.
- **Enhanced Readability**: The added indentation levels make it easy to follow the hierarchy or depth of operations in your logs.
- **Organized Logs**: Indentation allows you to group related log messages visually, making it easier to understand nested processes.
- **Easy Integration**: Seamlessly integrates with existing logging setups, requiring minimal changes to your current logging configuration.

## Features

- **Indentation Support**: Add indentation to your log messages based on the depth of operations, helping to clarify the structure of complex processes.
- **Custom Formatter**: Includes an `IndentFormatter` that automatically formats messages with the appropriate indentation.
- **Custom Logger Class**: Extends the standard logging `Logger` class to support managing indentation levels easily.
- **Dual Output**: Supports logging to both console and file, ensuring consistent formatting across all outputs.
- **Minimalist Design**: A simple, straightforward approach to enhancing your logging experience without unnecessary overhead.

## Installation

You can install IndentedLogger via pip:

```bash
pip install  indented_logger

