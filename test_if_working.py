import logging
import threading
from indented_logger import setup_logging, log_indent

# Configure logging
setup_logging(
    level=logging.DEBUG,
    include_func=True,
    truncate_messages=False,
    min_func_name_col=100,
    use_logger_hierarchy=True,
    indent_spaces=4
)

# Create hierarchical loggers
logger_root = logging.getLogger('app')
logger_module = logging.getLogger('app.module')
logger_submodule = logging.getLogger('app.module.submodule')

# Example 1: Basic logging with hierarchy-based indentation
def basic_logging_example():
    logger_root.info('Starting the application')
    logger_module.info('Initializing module')
    logger_submodule.info('Running submodule tasks')
    logger_module.info('Module completed')
    logger_root.info('Application finished')

# Example 2: Using manual indentation with 'lvl' parameter
def manual_indentation_example():
    logger = logging.getLogger('manual')
    logger.info('Manual indentation level 0', extra={'lvl': 0})
    logger.info('Manual indentation level 1', extra={'lvl': 1})
    logger.info('Manual indentation level 2', extra={'lvl': 2})
    logger.info('Back to level 1', extra={'lvl': 1})
    logger.info('Back to level 0', extra={'lvl': 0})

# Example 3: Using the @log_indent decorator
@log_indent
def decorated_function():
    logger = logging.getLogger('decorated')
    logger.info('Inside decorated function')
    nested_function()

@log_indent
def nested_function():
    logger = logging.getLogger('decorated.nested')
    logger.info('Inside nested function')

# Example 4: Combining hierarchy, decorators, and manual indentation
@log_indent
def complex_example():
    logger = logging.getLogger('app.complex')
    logger.info('Starting complex operation')
    logger.info('Manual indent inside decorator', extra={'lvl': 1})
    sub_operation()
    logger.info('Complex operation finished')

@log_indent
def sub_operation():
    logger = logging.getLogger('app.complex.sub')
    logger.info('Sub-operation in progress')

# Example 5: Demonstrating message truncation
def message_truncation_example():
    # Reconfigure logging with message truncation enabled
    setup_logging(
        level=logging.DEBUG,
        include_func=True,
        truncate_messages=True,
        min_func_name_col=100,
        use_logger_hierarchy=True,
        indent_spaces=4
    )
    logger = logging.getLogger('truncate')
    long_message = 'This is a very long log message that will be truncated to a maximum length for display purposes'
    logger.info(long_message)

# Example 6: Multi-threading to demonstrate thread safety
def threading_example():
    def worker(thread_id):
        logger = logging.getLogger(f'app.thread{thread_id}')
        logger.info(f'Thread {thread_id} starting work')
        @log_indent
        def thread_task():
            logger.info(f'Thread {thread_id} is working')
        thread_task()
        logger.info(f'Thread {thread_id} finished work')

    threads = []
    for i in range(2):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Run examples
if __name__ == '__main__':
    print("\n--- Example 1: Basic Logging with Hierarchy-based Indentation ---\n")
    basic_logging_example()

    print("\n--- Example 2: Manual Indentation with 'lvl' Parameter ---\n")
    manual_indentation_example()

    print("\n--- Example 3: Using the @log_indent Decorator ---\n")
    decorated_function()

    print("\n--- Example 4: Combining Hierarchy, Decorators, and Manual Indentation ---\n")
    complex_example()

    print("\n--- Example 5: Demonstrating Message Truncation ---\n")
    message_truncation_example()

    print("\n--- Example 6: Multi-threading to Demonstrate Thread Safety ---\n")
    threading_example()
