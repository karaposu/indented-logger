import logging
import functools
import threading

# -------------------------
# Thread-Local Indentation
# -------------------------

_thread_local = threading.local()


def get_indent_level():
    return getattr(_thread_local, 'indent_level', 0)


def increase_indent():
    _thread_local.indent_level = get_indent_level() + 1


def decrease_indent():
    current = get_indent_level()
    _thread_local.indent_level = current - 1 if current > 0 else 0


# -------------------------
# Logging Decorator
# -------------------------

def log_indent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_current_logger()
        # Pass the actual function name via 'extra'
        extra = {'funcNameOverride': func.__name__}
        logger.info(f"Entering function: {func.__name__}", extra=extra)
        increase_indent()
        try:
            return func(*args, **kwargs)
        finally:
            decrease_indent()
            logger.info(f"Exiting function: {func.__name__}", extra=extra)

    return wrapper


# -------------------------
# Logger Retrieval
# -------------------------

_current_logger = None


def get_current_logger():
    return _current_logger if _current_logger else logging.getLogger(__name__)


# -------------------------
# Custom Formatter
# -------------------------

class IndentFormatter(logging.Formatter):
    def __init__(self, include_func=False, truncate_messages=False, min_func_name_col=80, datefmt=None):
        self.include_func = include_func
        self.truncate_messages = truncate_messages
        self.min_func_name_col = min_func_name_col
        if include_func:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s%(padding)s{%(funcName)s}'
        else:
            fmt = '%(asctime)s - %(levelname)-8s - %(message)s'
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        # Use 'funcNameOverride' if provided
        func_name = getattr(record, 'funcNameOverride', record.funcName)
        record.funcName = func_name

        indent_level = get_indent_level()
        manual_indent = getattr(record, 'lvl', 0)
        total_indent = indent_level + manual_indent
        indent = ' ' * (total_indent * 4)

        # Original message with indentation
        message = f"{indent}{record.getMessage()}"

        # Handle message truncation if enabled
        if self.truncate_messages:
            max_message_length = 50  # or any desired length
            if len(message) > max_message_length:
                message = message[:max_message_length - 3] + '...'

        # Format asctime and levelname
        record.asctime = self.formatTime(record, self.datefmt)
        levelname = f"{record.levelname:<8}"

        # Build base log line and calculate its length
        base_log = f"{record.asctime} - {levelname} - {message}"

        if self.include_func:
            base_log_len = len(base_log)
            if base_log_len < self.min_func_name_col:
                spaces_needed = self.min_func_name_col - base_log_len
                record.padding = ' ' * spaces_needed
            else:
                record.padding = ' '
        else:
            record.padding = ''

        # Set the formatted message
        record.msg = message
        record.args = ()
        return super().format(record)


# -------------------------
# Custom Logger
# -------------------------

class CustomLogger(logging.Logger):
    def _log_with_indent(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if extra is None:
            extra = {}
        super()._log(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

    def _log_with_lvl(self, level, msg, args, **kwargs):
        stacklevel = kwargs.pop('stacklevel', 3)
        stack_info = kwargs.pop('stack_info', False)
        extra = kwargs.pop('extra', {})
        lvl = kwargs.pop('lvl', 0)
        exc_info = kwargs.pop('exc_info', None)
        if 'lvl' in extra:
            extra['lvl'] += lvl
        else:
            extra['lvl'] = lvl
        # Merge any remaining kwargs into extra, excluding reserved keys
        reserved_keys = ('exc_info', 'stack_info', 'stacklevel', 'extra', 'lvl')
        for key in kwargs:
            if key in reserved_keys:
                continue  # Skip reserved keys
            extra[key] = kwargs[key]
        self._log_with_indent(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

    def debug(self, msg, *args, **kwargs):
        self._log_with_lvl(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log_with_lvl(logging.INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log_with_lvl(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log_with_lvl(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log_with_lvl(logging.CRITICAL, msg, args, **kwargs)


# -------------------------
# Indented Logger Setup
# -------------------------

class IndentedLogger:
    def __init__(self, name, level=logging.DEBUG, log_file=None, include_func=False, truncate_messages=False,
                 min_func_name_col=80):
        global _current_logger
        logging.setLoggerClass(CustomLogger)
        self.logger = logging.getLogger(name)
        _current_logger = self.logger  # Store the logger globally for decorator access
        if not self.logger.handlers:
            self.logger.setLevel(level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = IndentFormatter(include_func=include_func, truncate_messages=truncate_messages,
                                                min_func_name_col=min_func_name_col)
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # File handler (if a log_file is specified)
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_formatter = IndentFormatter(include_func=include_func, truncate_messages=truncate_messages,
                                                 min_func_name_col=min_func_name_col)
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

            self.logger.propagate = False  # Prevent log messages from being propagated to the root logger

    def get_logger(self):
        return self.logger


# -------------------------
# Usage Example
# -------------------------

if __name__ == "__main__":
    # Initialize the IndentedLogger with function names included and min_func_name_col set
    indented_logger = IndentedLogger('my_logger', include_func=True, truncate_messages=False, min_func_name_col=100)
    logger = indented_logger.get_logger()


    @log_indent
    def start_process():
        logger.info('Starting process')
        load_data()
        another_function()


    @log_indent
    def load_data():
        logger.info('Loading data', lvl=1)
        logger.warning('Data format deprecated')
        try:
            # Simulate an error
            raise ValueError("Invalid data format")
        except ValueError as e:
            logger.error(f'Failed to load data: {e}', lvl=2, exc_info=True)
            logger.critical('System crash', exc_info=True)


    @log_indent
    def another_function():
        logger.info('Another function started')
        nested_function()


    @log_indent
    def nested_function():
        logger.debug('Inside nested function')
        logger.info('Nested function processing')


    # Start the logging process
    start_process()
