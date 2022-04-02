import traceback

from requests import Session, exceptions

from genius_lite.utils.logger import Logger
from genius_lite.utils.http import log_response, configured


class HttpRequest:
    def __init__(self, **spider_config):
        self.logger = Logger.instance()
        self.session = Session()
        self.default_timeout = spider_config.get('timeout') or 15

    @configured
    def request(self, **kwargs):
        return self.send(kwargs.get('request'), **kwargs.get('send_config'))

    @log_response
    def send(self, request, **kwargs):
        return self.session.send(request, **kwargs)

    def execute(self, seed):
        retry_count = 3
        while retry_count:
            try:
                response = self.request(seed = seed)
                return response
            except (exceptions.Timeout, exceptions.ConnectTimeout, exceptions.ReadTimeout):
                retry_count -= 1
                self.logger.warning('Timeout')
            except:
                self.logger.error(f'Error: {seed.url}\n{traceback.format_exc()}')
                break
        return None
