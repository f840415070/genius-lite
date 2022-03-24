import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from genius_lite.utils.colored_formatter import ColoredFormatter

log_format = '[%(levelname)s] %(asctime)s -> %(filename)s (line:%(lineno)d) -> %(name)s: %(message)s'


class Logger:
    __instance = None

    def __init__(self, name, **spider_config):
        self.enable = spider_config.get('log_enable') != False
        level = spider_config.get('log_level') or 'DEBUG'
        format = spider_config.get('log_format') or log_format
        output = spider_config.get('log_output')

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
            raise FileNotFoundError(f'Directory not found: {path}')

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
    def instance(cls, name=None, **spider_config):
        if not cls.__instance:
            cls.__instance = cls(name, **spider_config)
        return cls.__instance


if __name__ == '__main__':
    config = {}
    logger = Logger.instance('example', **config)
    logger.debug('it is a debug msg')
    logger.info('it is a info msg')
    logger.warning('it is a warning msg')
    logger.error('it is a error msg')
    logger.critical({'error': 'it is a critical msg'})
    logger2 = Logger.instance()
    logger2.info(id(logger) == id(logger2))
