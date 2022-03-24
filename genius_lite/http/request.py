import time
import traceback
import random
from requests import Session, Request, exceptions
from genius_lite.utils.logger import Logger
from genius_lite.http.user_agent_pool import UserAgentPool


class HttpRequest:
    def __init__(self, **spider_config):
        self.logger = Logger.instance()
        self.session = Session()
        self.default_timeout = spider_config.get('timeout') or 10

    def send(self, seed):
        request_config = self.request_config(seed)
        send_config = self.send_config(seed)
        request = self.session.prepare_request(Request(**request_config))
        self.logger.info(f'Start request: {seed.url}')
        if (send_config.get('proxies')):
            self.logger.info(f'Use Proxies: {send_config.get("proxies")}')

        ctime = time.time()
        resp = self.session.send(request, **send_config)
        self.logger.info(f'Response time: {int((time.time() - ctime) * 1000)}ms')
        return self.handle_resp(resp, seed.encoding or 'utf-8')

    def handle_resp(self, resp, encoding):
        if not resp:
            self.logger.warning('Response is None')
            return None
        resp.encoding = encoding
        resp.close()
        return resp

    def execute(self, seed):
        retry_count = 3
        while retry_count:
            try:
                response = self.send(seed)
                return response
            except (exceptions.Timeout, exceptions.ConnectTimeout, exceptions.ReadTimeout):
                retry_count -= 1
                self.logger.warning(f'Request timeout: {seed.url}')
                time.sleep(1)
            except:
                self.logger.error(f'Request failed: {seed.url}\n{traceback.format_exc()}')
                break
        return None

    def request_config(self, seed):
        if seed.headers is None:
            seed.headers = {
                'Accept': '*/*',
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        if not seed.headers.get('User-Agent'):
            seed.headers['User-Agent'] = random.choice(UserAgentPool)
        if not seed.method:
            seed.method = 'GET'

        config = {'method': seed.method, 'headers': seed.headers, 'url': seed.url,
                  'data': seed.data, 'params': seed.params, 'cookies': seed.cookies}
        config.update({
            'files': getattr(seed, 'files') if hasattr(seed, 'files') else None,
            'json': getattr(seed, 'json') if hasattr(seed, 'json') else None,
            'auth': getattr(seed, 'auth') if hasattr(seed, 'auth') else None,
            'hooks': getattr(seed, 'hooks') if hasattr(seed, 'hooks') else None,
        })
        return config

    def send_config(self, seed):
        return {
            'timeout': getattr(seed, 'timeout') if hasattr(seed, 'timeout') else self.default_timeout,
            'verify': getattr(seed, 'verify') if hasattr(seed, 'verify') else True,
            'stream': getattr(seed, 'stream') if hasattr(seed, 'stream') else False,
            'cert': getattr(seed, 'cert') if hasattr(seed, 'cert') else None,
            'allow_redirects': getattr(seed, 'allow_redirects') if hasattr(seed, 'allow_redirects') else True,
            'proxies': getattr(seed, 'proxies') if hasattr(seed, 'proxies') else None
        }
