import logging

class IndentFormatter(logging.Formatter):
    def format(self, record):
        indent_level = getattr(record, 'lvl', 0)
        indent = ' ' * (indent_level * 4)
        record.msg = f"{indent}{record.msg}"
        return super().format(record)

class CustomLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if extra is None:
            extra = {}
        if 'lvl' not in extra:
            extra['lvl'] = 0
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

class IndentedLogger:
    def __init__(self, name, level=logging.DEBUG, log_file=None):
        logging.setLoggerClass(CustomLogger)
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = IndentFormatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # File handler (if a log_file is specified)
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_formatter = IndentFormatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

            self.logger.propagate = False

    def get_logger(self):
        return self.logger
