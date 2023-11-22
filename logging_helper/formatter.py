
import logging

class TestingLogFormatter(logging.Formatter):
    reset = "\x1b[0m"
    color_ascname = "\x1b[38;5;99m{}" + reset
    color_name = "\x1b[38;5;39m{}" + reset
    color_debug = "\x1b[38;5;11m{}" + reset
    color_info = "\x1b[38;5;15m{}" + reset
    color_warning = "\x1b[38;5;226m{}" + reset
    color_error = "\x1b[38;5;196m{}" + reset
    color_critical = "\x1b[38;5;201m{}" + reset
    color_threadName = "\x1b[38;5;82m{}" + reset

    fmt_asctime = color_ascname.format("[%(asctime)s]")
    fmt_name = color_name.format("[%(name)s]")
    fmt_threadName = color_threadName.format("[%(threadName)s]")

    fmt = fmt_asctime + fmt_name + fmt_threadName

    FORMATS = {
        logging.DEBUG: fmt + color_debug.format("[%(levelname)s] %(message)s"),
        logging.INFO: fmt + color_info.format("[%(levelname)s] %(message)s"),
        logging.WARNING: fmt + color_warning.format("[%(levelname)s] %(message)s"),
        logging.ERROR: fmt + color_error.format("[%(levelname)s] %(message)s"),
        logging.CRITICAL: fmt + color_critical.format("[%(levelname)s] %(message)s"),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class UvicornDefaultFormatter(logging.Formatter):
    reset = "\x1b[0m"
    color_ascname = "\x1b[38;5;99m{}" + reset
    color_name = "\x1b[38;5;39m{}" + reset
    color_debug = "\x1b[38;5;11m{}" + reset
    color_info = "\x1b[38;5;15m{}" + reset
    color_warning = "\x1b[38;5;226m{}" + reset
    color_error = "\x1b[38;5;196m{}" + reset
    color_critical = "\x1b[38;5;201m{}" + reset
    color_threadName = "\x1b[38;5;82m{}" + reset

    fmt_asctime = color_ascname.format("[%(asctime)s]")
    fmt_name = color_name.format("[%(name)s]")
    fmt_threadName = color_threadName.format("[%(threadName)s]")

    fmt = fmt_asctime + fmt_name + fmt_threadName

    FORMATS = {
        logging.DEBUG: fmt + color_debug.format("[%(levelname)s] %(message)s"),
        logging.INFO: fmt + color_info.format("[%(levelname)s] %(message)s"),
        logging.WARNING: fmt + color_warning.format("[%(levelname)s] %(message)s"),
        logging.ERROR: fmt + color_error.format("[%(levelname)s] %(message)s"),
        logging.CRITICAL: fmt + color_critical.format("[%(levelname)s] %(message)s"),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class UvicornAccessFormatter(logging.Formatter):
    reset = "\x1b[0m"
    color_ascname = "\x1b[38;5;99m{}" + reset
    color_name = "\x1b[38;5;39m{}" + reset
    color_debug = "\x1b[38;5;11m{}" + reset
    color_info = "\x1b[38;5;15m{}" + reset
    color_warning = "\x1b[38;5;226m{}" + reset
    color_error = "\x1b[38;5;196m{}" + reset
    color_critical = "\x1b[38;5;201m{}" + reset
    color_threadName = "\x1b[38;5;82m{}" + reset

    fmt_asctime = color_ascname.format("[%(asctime)s]")
    fmt_name = color_name.format("[%(name)s]")
    fmt_threadName = color_threadName.format("[%(threadName)s]")

    fmt = fmt_asctime + fmt_name + fmt_threadName

    FORMATS = {
        logging.DEBUG: fmt + color_debug.format("[%(levelname)s] %(message)s"),
        logging.INFO: fmt + color_info.format("[%(levelname)s] %(message)s"),
        logging.WARNING: fmt + color_warning.format("[%(levelname)s] %(message)s"),
        logging.ERROR: fmt + color_error.format("[%(levelname)s] %(message)s"),
        logging.CRITICAL: fmt + color_critical.format("[%(levelname)s] %(message)s"),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)