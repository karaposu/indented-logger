# Guide to Setting Up Logging in a Multi-Module Python Application

Proper logging is essential for monitoring, debugging, and maintaining applications, especially as they grow in complexity with multiple modules and packages. This guide will walk you through best practices for setting up logging in a Python application with many modules, incorporating features from the `indented_logger` package for enhanced readability.

---

## Table of Contents

1. **Introduction**
2. **Logging Best Practices in Multi-Module Applications**
3. **Using Module-Level Loggers**
4. **Configuring Logging with `indented_logger`**
5. **Handling Modules Run Directly**
6. **Avoiding Side Effects in Logging Configuration**
7. **Putting It All Together: A Practical Example**
8. **Additional Tips and Recommendations**
9. **Conclusion**

---

## 1. Introduction

Logging is a critical component of any application. It provides insights into the application's behavior, helps diagnose issues, and aids in understanding the flow of execution. In multi-module applications, proper logging setup ensures that logs are organized, readable, and provide sufficient context.

The `indented_logger` package enhances Python's standard logging by introducing automatic and manual indentation, making logs more readable and structured.

---

## 2. Logging Best Practices in Multi-Module Applications

- **Use Module-Level Loggers**: Create a logger in each module using `logging.getLogger(__name__)`. This ensures that logger names reflect the module hierarchy.
- **Avoid Passing Loggers Between Modules**: Passing the same logger instance can lead to loss of context and interfere with features that rely on logger names.
- **Configure Logging in the Main Entry Point**: Centralize logging configuration in the main script to avoid conflicts and maintain consistency.
- **Avoid Side Effects**: Do not configure logging at the module level to prevent unintended side effects when modules are imported.
- **Handle Modules Run Directly**: Ensure that logging is properly configured when modules are executed as scripts.

---

## 3. Using Module-Level Loggers

Creating a logger in each module allows you to:

- **Reflect Module Hierarchy**: Logger names match the module's import path.
- **Leverage Hierarchy-Based Indentation**: With `indented_logger`, indentation levels are based on the logger's name hierarchy.
- **Maintain Context**: Logs include information about the module and function where they originated.

**Example:**

```python
# In each module (e.g., module1.py)
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.info('This is a log message from module1')
```

---

## 4. Configuring Logging with `indented_logger`

The `indented_logger` package provides enhanced formatting and indentation features.

### Installing `indented_logger`

```bash
pip install indented_logger
```

### Setting Up Logging Configuration

Configure logging in your main script using the `setup_logging` function.

**Parameters:**

- `level`: Logging level (e.g., `logging.INFO`).
- `include_func`: Include function names in logs.
- `include_module`: Include module names in logs.
- `func_module_format`: Format string for combining function and module names.
- `use_logger_hierarchy`: Indent logs based on logger hierarchy.
- `indent_spaces`: Number of spaces per indentation level.
- `min_func_name_col`: Column at which function/module names should start.

**Example:**

```python
# main.py
from indented_logger import setup_logging

setup_logging(
    level=logging.INFO,
    include_func=True,
    include_module=True,
    func_module_format='{moduleName}:{funcName}',
    use_logger_hierarchy=True,
    indent_spaces=4,
    min_func_name_col=80
)
```

---

## 5. Handling Modules Run Directly

To ensure that logging works correctly when modules are run directly:

1. **Add a `main()` Function**: Define a `main()` function in each module that might be executed directly.
2. **Configure Logging in `main()`**: Include logging configuration within the `main()` function.
3. **Check `__name__ == '__main__'`**: Run the `main()` function only when the module is executed as the main script.

**Example:**

```python
# module1.py
import logging
import module2  # Import other modules as needed

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
        include_module=True,
        func_module_format='{moduleName}:{funcName}',
        use_logger_hierarchy=True
    )
    logger.info('Running module1 as main')
    module1_function()

if __name__ == '__main__':
    main()
```

---

## 6. Avoiding Side Effects in Logging Configuration

- **Configure Logging Only When Necessary**: Place logging setup inside the `main()` function or under `if __name__ == '__main__'` to prevent it from executing during imports.
- **Prevent Multiple Configurations**: Ensure that logging configuration is not applied multiple times or from multiple places to avoid conflicts.

---

## 7. Putting It All Together: A Practical Example

### Project Structure

```
my_app/
├── main.py
├── module1/
│   ├── __init__.py
│   └── module1.py
├── module2/
│   ├── __init__.py
│   └── module2.py
└── indented_logger/  # The indented_logger package
```

### `main.py`

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

### `module1/module1.py`

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

### `module2/module2.py`

```python
import logging

logger = logging.getLogger(__name__)

def module2_function():
    logger.info('Entered module2_function')
    # Simulate work
    logger.info('Performing computations...')
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

### Expected Output

When running `main.py`, the logs will show hierarchical indentation based on the module structure and function calls.

**Sample Output:**

```
2024-10-15 17:27:51,032 - INFO     - Starting main function                               {__main__:main}
2024-10-15 17:27:51,032 - INFO     -     Entered module1_function                         {module1.module1:module1_function}
2024-10-15 17:27:51,032 - INFO     -         Entered module2_function                     {module2.module2:module2_function}
2024-10-15 17:27:51,032 - INFO     -         Performing computations...                   {module2.module2:module2_function}
2024-10-15 17:27:51,032 - INFO     -         Exiting module2_function                     {module2.module2:module2_function}
2024-10-15 17:27:51,032 - INFO     -     Exiting module1_function                         {module1.module1:module1_function}
2024-10-15 17:27:51,032 - INFO     - Finished main function                               {__main__:main}
```

---

## 8. Additional Tips and Recommendations

### Using the `@log_indent` Decorator

The `indented_logger` provides a `@log_indent` decorator to automatically manage indentation levels based on function calls.

**Example:**

```python
from indented_logger import log_indent

@log_indent
def some_function():
    logger.info('This is an indented message')
```

### Manual Indentation with `lvl`

You can manually adjust indentation levels using the `lvl` parameter in logging calls.

```python
logger.info('Manually indented message', extra={'lvl': 2})
```

### Customizing Indentation Spaces

Adjust the number of spaces per indentation level using the `indent_spaces` parameter in `setup_logging`.

```python
setup_logging(
    indent_spaces=2,  # Default is 4
    # Other parameters...
)
```

### Formatting Function and Module Names

Customize how function and module names are displayed using the `func_module_format` parameter.

```python
setup_logging(
    func_module_format='{moduleName}:{funcName}',  # Custom format
    # Other parameters...
)
```

### Avoiding Multiple Logging Configurations

- **Centralize Configuration**: Configure logging in a single place when possible.
- **Use Conditional Configuration**: Apply logging setup only when modules are run directly.

---

## 9. Conclusion

Setting up logging correctly in a multi-module application ensures that logs are informative, structured, and easy to read. By following best practices such as using module-level loggers, configuring logging appropriately, and leveraging features from the `indented_logger` package, you can enhance the readability and maintainability of your application's logs.

---

## Summary of Key Points

- **Module-Level Loggers**: Use `logging.getLogger(__name__)` in each module.
- **Hierarchy-Based Indentation**: Enable `use_logger_hierarchy=True` to indent logs based on the logger's name hierarchy.
- **Configure Logging in Main Scripts**: Set up logging in the main entry point of your application.
- **Handle Modules Run Directly**: Include a `main()` function and configure logging within it.
- **Avoid Side Effects**: Prevent logging configuration from executing during module imports.
- **Customize Logging Output**: Use parameters like `include_func`, `include_module`, and `func_module_format` for flexible log formatting.

---


## 1. Best Practices for Logging in Libraries (PyPI Packages)

When writing a library or package intended for others to use, it's important to follow logging best practices to avoid interfering with the user's application logging configuration.

### **A. Do Not Configure Logging Handlers or Levels in Libraries**

- **Avoid Adding Handlers:** Libraries should not add handlers (like `StreamHandler` or `FileHandler`) to loggers. Adding handlers at the library level can lead to duplicate log messages or unexpected logging behavior in the user's application.
  
- **Avoid Setting Logger Levels:** Libraries should not set logging levels for loggers (`logger.setLevel`). This should be left to the user's application to configure.

**Your module-level logging configuration should be removed or limited to the `if __name__ == "__main__":` block.**

### **B. Use Module-Level Loggers Without Configuration**

In your library code, you should obtain a logger using `logging.getLogger(__name__)` and use it without adding handlers or setting levels.


## Further Reading and Resources

- **Python Logging Documentation**: [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)
- **`indented_logger` Package**: Documentation and usage examples provided in the package's README.
- **Best Practices for Python Logging**: Articles and tutorials on effective logging strategies in Python applications.

---





