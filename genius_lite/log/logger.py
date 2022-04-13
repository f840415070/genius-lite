import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from genius_lite.log.colored_formatter import ColoredFormatter

formatter = ColoredFormatter(
    fmt='%(log_color)s%(levelname)-7s %(white)s%(asctime)s %(reset)s-> '
        '%(white)s%(name)s %(reset)s-> %(message_log_color)s%(message)s',
    reset=True,
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red'
    },
    secondary_log_colors={
        'message': {
            'DEBUG': 'blue',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    }
)
file_formatter = logging.Formatter(
    fmt='%(levelname)-7s %(asctime)s -> %(name)s -> %(message)s',
)


class Logger:
    __instance = None

    def __init__(self, name, **log_config):
        self.enable = log_config.get('enable') != False
        level = log_config.get('level') or 'DEBUG'
        output = log_config.get('output')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if self.enable:
            self.logger.addHandler(self.stream_handler(level))
            if output:
                self.check_output_path(output)
                self.logger.addHandler(self.file_handler(name, level, output))

        self.logger.propagate = False

    def stream_handler(self, level):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    def file_handler(self, name, level, output):
        filename = os.path.join(output, ''.join([name, '.log']))
        handler = TimedRotatingFileHandler(filename=filename, when='MIDNIGHT', backupCount=3,
                                           interval=1, encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(file_formatter)
        return handler

    def check_output_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError('Directory not found: %s' % path)

    @property
    def debug(self):
        return self.logger.debug if self.enable else self.notset

    @property
    def info(self):
        return self.logger.info if self.enable else self.notset

    @property
    def warning(self):
        return self.logger.warning if self.enable else self.notset

    @property
    def error(self):
        return self.logger.error if self.enable else self.notset

    def notset(self, msg, *args, **kwargs):
        pass

    @classmethod
    def instance(cls, name=None, **log_config):
        if not cls.__instance:
            cls.__instance = cls(name, **log_config)
        return cls.__instance
