import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from genius_lite.log.colored_formatter import ColoredFormatter

log_format = '[%(levelname)s] %(asctime)s -> %(name)s: %(message)s'


class Logger:
    __instance = None

    def __init__(self, name, **log_config):
        self.enable = log_config.get('enable') != False
        level = log_config.get('level') or 'DEBUG'
        format = log_config.get('format') or log_format
        output = log_config.get('output')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if self.enable:
            self.logger.addHandler(self.stream_handler(level, format))
            if output:
                self.check_output_path(output)
                self.logger.addHandler(self.file_handler(name, level, format, output))

        self.logger.propagate = False

    def stream_handler(self, level, format):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(ColoredFormatter(fmt='%(log_color)s' + format))
        return handler

    def file_handler(self, name, level, format, output):
        filename = os.path.join(output, ''.join([name, '.log']))
        handler = TimedRotatingFileHandler(filename=filename, when='MIDNIGHT', backupCount=3,
                                           interval=1, encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
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

    @property
    def critical(self):
        return self.logger.critical if self.enable else self.notset

    def notset(self, msg, *args, **kwargs):
        pass

    @classmethod
    def instance(cls, name=None, **log_config):
        if not cls.__instance:
            cls.__instance = cls(name, **log_config)
        return cls.__instance
