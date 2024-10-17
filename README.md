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

______

For detailed documentation which talks about best practices and limitations, see [Dive deep in to loggers](learn_more_about_loggers.md).
______



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

### Automatic Child Logger Indentation ( indent packages )

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
    indent_packages=True
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


  
### Aligning Function Names at a Specific Column

Align function and module names at a specified column using the `min_func_name_col` parameter.

```python
# Setup the logger with alignment at column 100
setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=True,
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

---------

## Introduction

In logging, indentation can be a powerful tool to represent the hierarchical structure of your application's execution flow. It helps in understanding which functions or modules are calling others and how deep into the execution stack you are at any point.

However, automatically indenting logs based on module transitions during application flow is not feasible due to the stateless nature of the logging system and the complexities involved in tracking dynamic execution paths. Instead, **Indented Logger** provides a safe and compatible way to achieve similar results by offering:

- **Automatic indentation based on module and package hierarchy**
- **Manual indentation control using decorators**

## Why Automatic Indentation Based on Module Transitions Isn't Feasible

In a perfect Python world, we might wish for logs to automatically indent whenever the execution flow moves from one module to another. However, this approach faces several challenges:

1. **Stateless Logging System**: The Python logging module processes each log record independently without retaining state between records. It doesn't track the execution flow or module transitions over time.

2. **Concurrency Issues**: In multi-threaded applications, logs from different threads and modules can interleave. Tracking module transitions globally can lead to incorrect indentation and confusion.

3. **Complex Execution Paths**: Applications often have dynamic and non-linear execution flows. Modules may call each other in various orders, making it difficult to determine indentation solely based on module transitions.

Due to these reasons, automatically indenting logs based on module transitions isn't practical or reliable.

## Achieving Hierarchical Indentation

To represent the hierarchical structure of your application's execution flow effectively, **Indented Logger** provides three mechanisms:

1. **Automatic Indentation Based on Module Hierarchy (`indent_modules`)**
2. **Automatic Indentation Based on Package Hierarchy (`indent_packages`)**
3. **Manual Indentation Control Using Decorators (`@log_indent`)**

### Indentation Parameters

#### 1. `indent_modules` (Boolean)

- **Purpose**: Indents logs from any module that is not the main module (`__main__`).
- **Usage**: Set to `True` to enable indentation for all non-main modules.
- **Example**:
  ```python
  setup_logging(indent_modules=True)
  ```

#### 2. `indent_packages` (Boolean)

- **Purpose**: Indents logs based on the package hierarchy by counting the number of dots in the module's name.
- **Usage**: Set to `True` to enable indentation based on package depth.
- **Example**:
  ```python
  setup_logging(indent_packages=True)
  ```

### Using Decorators for Function Call Hierarchy

#### `@log_indent`

- **Purpose**: Manually control indentation to reflect the function call hierarchy.
- **Usage**: Decorate functions where you want to increase the indentation level upon entry and decrease it upon exit.
- **Example**:
  ```python
  from indented_logger import log_indent

  @log_indent
  def my_function():
      logger.info("Inside my_function")
  ```

By combining these mechanisms, you can achieve a comprehensive and accurate representation of both your application's static structure (modules and packages) and dynamic execution flow (function calls).


### Semi-Auto Indentation Example

Consider the following project structure:

```
my_app/
├── main.py
├── module_a.py
└── package_b/
    ├── __init__.py
    ├── module_b1.py
    └── module_b2.py
```

#### `main.py`

```python
from indented_logger import setup_logging
import logging
import module_a
from package_b import module_b1

def main():
    logger = logging.getLogger(__name__)
    logger.info("Starting main")
    module_a.func_a()
    module_b1.func_b1()

if __name__ == '__main__':
    setup_logging(
        level=logging.DEBUG,
        include_func=True,
        include_module=True,
        indent_modules=True,
        indent_packages=True,
        indent_spaces=4
    )
    main()
```

#### `module_a.py`

```python
import logging

logger = logging.getLogger(__name__)

def func_a():
    logger.info("Inside func_a")
```

#### `package_b/module_b1.py`

```python
import logging
from indented_logger import log_indent
from package_b import module_b2

logger = logging.getLogger(__name__)

@log_indent
def func_b1():
    logger.info("Inside func_b1")
    module_b2.func_b2()
```

#### `package_b/module_b2.py`

```python
import logging
from indented_logger import log_indent

logger = logging.getLogger(__name__)

@log_indent
def func_b2():
    logger.info("Inside func_b2")
```

#### Running the Application

When you run `main.py`, the output will be:

```
2024-10-16 21:55:26,908 - INFO     - Starting main                              {__main__:main}
2024-10-16 21:55:26,909 - INFO     -     Inside func_a                          {module_a:func_a}
2024-10-16 21:55:26,910 - INFO     -     Inside func_b1                         {package_b.module_b1:func_b1}
2024-10-16 21:55:26,911 - INFO     -         Inside func_b2                     {package_b.module_b2:func_b2}
```

- Logs from `module_a.py` are indented by one level due to `indent_modules=True`.
- Logs from `module_b1.py` are indented further due to `indent_packages=True` and the use of `@log_indent`.
- Logs from `module_b2.py` are indented even more, reflecting both the package depth and the function call hierarchy.

## Customization

You can customize the behavior of **Indented Logger** using various parameters in `setup_logging`:

- `level`: Set the logging level (e.g., `logging.DEBUG`, `logging.INFO`).
- `include_func`: Include function names in the log output.
- `include_module`: Include module names in the log output.
- `func_module_format`: Customize the format of the function and module information.
- `indent_spaces`: Set the number of spaces per indentation level.
- `truncate_messages`: Enable truncation of long messages.
- `min_func_name_col`: Column position where function/module names should start.
- `debug`: Enable debug mode for troubleshooting.

## Conclusion

While automatic indentation based on module transitions during application flow isn't feasible due to technical limitations, **Indented Logger** provides a robust and flexible solution to represent both your application's structure and execution flow.

By leveraging:

- **Automatic indentation based on module and package hierarchy** (`indent_modules`, `indent_packages`)
- **Manual control over function call hierarchy using decorators** (`@log_indent`)

You can create clear, organized, and hierarchical log outputs that significantly enhance readability and make debugging easier.





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





