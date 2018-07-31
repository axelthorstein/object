import sys
import logging
from contextlib import contextmanager


def _stdout_is_a_tty():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


if _stdout_is_a_tty():
    import colorlog
    FORMATTER = colorlog.ColoredFormatter(
        '%(bold)s%(asctime)s.%(msecs)03d %(log_color)s%(levelname)s %(reset)s%(bold)s%(name)s %(message_log_color)s%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        })
else:
    FORMATTER = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

OBJECT_LOGGER = logging.getLogger('object')
OBJECT_LOGGER.setLevel(logging.INFO)

# Add the console handler to the root logger
_CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
_CONSOLE_HANDLER.setFormatter(FORMATTER)

OBJECT_LOGGER.parent.addHandler(_CONSOLE_HANDLER)


def logger(name):
    return logging.getLogger(name)


class LogMixin:

    @property
    def logger(self):
        name = '.'.join(['object', self.__class__.__name__])
        return logger(name)

    @contextmanager
    def silence_logging(self):
        self.logger.propagate = False
        yield
        self.logger.propagate = True
