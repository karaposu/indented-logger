# indented_logger

**indented_logger** is a **custom formatter** for Python's standard `logging` package that adds **automatic indentation** and enhanced formatting support. It visually represents the hierarchical structure and depth of your logging messages, making it easier to understand the flow of execution in complex systems, **without altering the original logger class or causing any compatibility issues**.

## Features

- **Automatic Indentation via Decorators**: Use decorators to automatically manage indentation levels based on function call hierarchy.
- **Manual Indentation Support with `lvl`**: Add manual indentation to specific log messages for granular control using the `lvl` parameter.
- **Hierarchy-Based Indentation**: Indent logs automatically based on the logger's name hierarchy.
- **Customizable Function and Module Names**: Choose to include function names, module names, or both in your log messages, with flexible formatting options.
- **Function Name Alignment**: Align function and module names at a specified column for consistent and readable logs.
- **Message Truncation (Optional)**: Optionally truncate long messages to a specified length.
- **Thread Safety**: Manages indentation levels per thread, ensuring correct behavior in multi-threaded applications.
- **Easy Integration**: Seamlessly integrates with existing logging setups with minimal changes.

## Installation

You can install `indented_logger` via pip:

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

# Basic logging
logger.info('Starting process A')
# Manual indentation
logger.info('Details of process A', extra={'lvl': 1})
logger.info('Deeper Details of process A', extra={'lvl': 2})
logger.info('Process complete')
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - Starting process A                          {main}
2024-08-15 12:34:56 - INFO     -     Details of process A                    {main}
2024-08-15 12:34:56 - INFO     -         Deeper Details of process A         {main}
2024-08-15 12:34:56 - INFO     - Process complete                            {main}
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

### Automatic Child Logger Indentation

if enabled, **automatically adjusts the indentation of child loggers based on their relationship to the parent logger**. 
This is especially useful in multi-module applications, ensuring that log output is structured and clearly reflects the nested hierarchy of 
loggers and processes.

```python
from indented_logger import setup_logging
import logging

# Enable hierarchy-based indentation
setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=False,
    func_module_format='{funcName}',
    use_logger_hierarchy=True
)
# Create hierarchical loggers
logger_root = logging.getLogger('myapp')
logger_submodule = logging.getLogger('myapp.submodule')

def main():
    logger_root.info('Starting application')
    process_submodule()
    logger_root.info('Application finished')
    
def process_submodule():
    logger_submodule.info('Processing submodule task 1 ')
    logger_submodule.info('Processing submodule task 2 ')
    
if __name__ == '__main__':
    main()
```
**Output:**
```
2024-10-15 20:26:43,340 - INFO     - Starting application                       {main}
2024-10-15 20:26:43,340 - INFO     -     Processing submodule task 1            {process_submodule}
2024-10-15 20:26:43,340 - INFO     -     Processing submodule task 2            {process_submodule}
2024-10-15 20:26:43,340 - INFO     - Application finished                       {main}
```

**Note:** Replace `<function_name>` with the actual function name if `include_func` is `True`.

### Customizing Function and Module Names

You can customize the inclusion and formatting of function and module names using parameters.

```python
# Setup the logger with custom formatting
setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=True,
    func_module_format='{moduleName}:{funcName}',  # Customize as needed
    min_func_name_col=80
)
```

- **Parameters:**
  - `include_func` (bool): Include function names in logs.
  - `include_module` (bool): Include module names in logs.
  - `func_module_format` (str): Format string for combining function and module names. Placeholders `{funcName}` and `{moduleName}` are available.

### Aligning Function Names at a Specific Column

Align function and module names at a specified column using the `min_func_name_col` parameter.

```python
# Setup the logger with alignment at column 100
setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=True,
    func_module_format='{moduleName}:{funcName}',
    min_func_name_col=100
)
```

**Output:**

```
2024-08-15 12:34:56 - INFO     -     This is a log message                       {moduleName:funcName}
```

### Message Truncation (Optional)

Enable message truncation by setting the `truncate_messages` parameter to `True`.

```python
# Setup the logger with message truncation enabled
setup_logging(level=logging.INFO, truncate_messages=True)

logger = logging.getLogger(__name__)

logger.info('This is a very long log message that will be truncated to a maximum length')
```

**Output:**

```
2024-08-15 12:34:56 - INFO     - This is a very long log message th...    {main}
```

### Thread Safety

`indented_logger` uses thread-local storage to manage indentation levels per thread, ensuring correct behavior in multi-threaded applications.

### Handling Modules Run Directly

When you have modules that can be run directly (e.g., via `python -m module1`), ensure that `indented_logger` is configured in the `main()` function of the module.

```python
# module1.py

import logging
import module2

logger = logging.getLogger(__name__)

def module1_function():
    logger.info('Entered module1_function')
    module2.module2_function()
    logger.info('Exiting module1_function')

def main():
    from indented_logger import setup_logging
    setup_logging(
        level=logging.INFO,
        include_func=True,
        use_logger_hierarchy=True
    )
    logger.info('Running module1 as main')
    module1_function()

if __name__ == '__main__':
    main()
```

## Advanced Usage

### Setting Up Logging in Multi-Module Applications

Follow best practices for logging in multi-module applications:

1. **Use Module-Level Loggers**: In each module, create a logger using `logger = logging.getLogger(__name__)`.
2. **Configure Logging in Main Scripts**: Set up logging in the main entry point of your application.
3. **Handle Modules Run Directly**: Include a `main()` function and configure logging within it for modules that can be run directly.
4. **Avoid Side Effects**: Prevent logging configuration from executing during module imports.

### Example Project Structure

```
my_app/
├── main.py
├── module1/
│   ├── __init__.py
│   └── module1.py
├── module2/
│   ├── __init__.py
│   └── module2.py
```

**`main.py`:**

```python
import logging
from indented_logger import setup_logging
from module1.module1 import module1_function

# Configure logging
setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=True,
    func_module_format='{moduleName}:{funcName}',
    use_logger_hierarchy=True,
    indent_spaces=4,
    min_func_name_col=80
)

logger = logging.getLogger(__name__)

def main():
    logger.info('Starting main function')
    module1_function()
    logger.info('Finished main function')

if __name__ == '__main__':
    main()
```

**`module1/module1.py`:**

```python
import logging
from module2.module2 import module2_function

logger = logging.getLogger(__name__)

def module1_function():
    logger.info('Entered module1_function')
    module2_function()
    logger.info('Exiting module1_function')

def main():
    from indented_logger import setup_logging
    setup_logging(
        level=logging.INFO,
        include_func=True,
        include_module=True,
        func_module_format='{moduleName}:{funcName}',
        use_logger_hierarchy=True
    )
    logger.info('Running module1 as main')
    module1_function()

if __name__ == '__main__':
    main()
```

**`module2/module2.py`:**

```python
import logging

logger = logging.getLogger(__name__)

def module2_function():
    logger.info('Entered module2_function')
    # Perform some operations
    logger.info('Exiting module2_function')

def main():
    from indented_logger import setup_logging
    setup_logging(
        level=logging.INFO,
        include_func=True,
        include_module=True,
        func_module_format='{moduleName}:{funcName}',
        use_logger_hierarchy=True
    )
    logger.info('Running module2 as main')
    module2_function()

if __name__ == '__main__':
    main()
```

### Running the Application

- **Run the Main Application:**

  ```bash
  python main.py
  ```

- **Run `module1.py` Directly:**

  ```bash
  python -m module1.module1
  ```

- **Run `module2.py` Directly:**

  ```bash
  python -m module2.module2
  ```

**Expected Output:**

```
2024-08-15 12:34:56 - INFO     - Starting main function                               {__main__:main}
2024-08-15 12:34:56 - INFO     -     Entered module1_function                         {module1.module1:module1_function}
2024-08-15 12:34:56 - INFO     -         Entered module2_function                     {module2.module2:module2_function}
2024-08-15 12:34:56 - INFO     -         Exiting module2_function                     {module2.module2:module2_function}
2024-08-15 12:34:56 - INFO     -     Exiting module1_function                         {module1.module1:module1_function}
2024-08-15 12:34:56 - INFO     - Finished main function                               {__main__:main}
```

## Parameters for `setup_logging`

- `level` (int): Logging level (e.g., `logging.INFO`, `logging.DEBUG`).
- `include_func` (bool, optional): Include function names in log messages. Default is `False`.
- `include_module` (bool, optional): Include module names in log messages. Default is `False`.
- `func_module_format` (str, optional): Format string for combining function and module names. Default is `'{funcName}'`.
  - Placeholders:
    - `{funcName}`: Function name.
    - `{moduleName}`: Module (logger) name.
- `truncate_messages` (bool, optional): Truncate long messages. Default is `False`.
- `min_func_name_col` (int, optional): Column at which function/module names should start. Default is `80`.
- `use_logger_hierarchy` (bool, optional): Indent logs based on the logger's name hierarchy. Default is `False`.
- `indent_spaces` (int, optional): Number of spaces per indentation level. Default is `4`.
- `datefmt` (str, optional): Date format string.

### Example with All Parameters

```python
setup_logging(
    level=logging.DEBUG,
    include_func=True,
    include_module=True,
    func_module_format='{moduleName}:{funcName}',
    truncate_messages=False,
    min_func_name_col=100,
    use_logger_hierarchy=True,
    indent_spaces=4,
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

## Benefits

- **Enhanced Readability**: Visually represent the hierarchy and depth of operations in your logs.
- **Organized Logs**: Group related log messages, making it easier to understand nested processes.
- **Simplicity**: Minimalistic design adds just what you need without altering core logging functionalities.
- **Customizable Formatting**: Control inclusion of function names, module names, alignment, and message truncation.
- **Easy Integration**: Works with existing logging setups with minimal changes to your configuration.
- **Flexible Indentation**: Supports automatic indentation via hierarchy and decorators, as well as manual indentation.

## License

`indented_logger` is released under the [MIT License](LICENSE).

---

*Note: If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.*

---

## Additional Details

### Customizing Indentation and Formatting

- **Adjust Indentation Width**: Use the `indent_spaces` parameter in `setup_logging` to change the number of spaces per indentation level.
- **Set Date Format**: Pass a `datefmt` parameter to customize the timestamp format.

### Thread Safety

`indented_logger` uses thread-local storage to manage indentation levels per thread, ensuring that logs from different threads are correctly indented.

### Advanced Usage

For advanced use cases, you can extend or modify the `IndentFormatter` class to suit your specific requirements.

---

## Contributions and Support

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For support or questions, feel free to open an issue on GitHub.

---

Thank you for using `indented_logger`! We hope it enhances your logging experience and makes debugging and monitoring your applications more efficient.