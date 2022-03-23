import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

class Logger:
    __instance = None

    def __init__(self, name, **kwargs):
        self.__enable = kwargs.get('log_enable') != False
        level = kwargs.get('log_level') or 'INFO'
        format = kwargs.get('log_format') or '%(asctime)s - %(levelname)s - %(name)s: %(message)s'
        output = kwargs.get('log_output')

        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)

        if self.__enable:
            self.__logger.addHandler(self.stream_handler(level, format))
            if output:
                self.check_output_path(output)
                self.__logger.addHandler(self.file_handler(name, level, format, output))

        self.__logger.propagate = False

    def stream_handler(self, level, format):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
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

    def debug(self, msg):
        if self.__enable:
            self.__logger.debug(msg)

    def info(self, msg):
        if self.__enable:
            self.__logger.info(msg)

    def warning(self, msg):
        if self.__enable:
            self.__logger.warning(msg)

    def error(self, msg):
        if self.__enable:
            self.__logger.error(msg)

    @classmethod
    def instance(cls, name = None, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(name, **kwargs)
        return cls.__instance


if __name__ == '__main__':
    config = {
        # 'log_enable': False,
        'log_level': 'DEBUG',
    }
    logger = Logger.instance('example', **config)
    logger.debug('it is a debug msg')
    logger.info('it is a info msg')
    logger.warning('it is a warning msg')
    logger.error('it is a error msg')
