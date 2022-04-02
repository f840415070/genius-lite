import time
import random
from requests import Request
from genius_lite.utils.logger import Logger


def default_headers():
    return {
        'Accept': '*/*',
        "Accept-Encoding": "gzip, deflate",
        'Connection': 'keep-alive',
    }


def getUA():
    return random.choice(UserAgentPool)


def request_config(seed):
    if not seed.headers or not isinstance(seed.headers, dict):
        seed.headers = default_headers()
    if not seed.headers.get('User-Agent'):
        seed.headers['User-Agent'] = getUA()

    config = {'method': seed.method, 'headers': seed.headers, 'url': seed.url,
              'data': seed.data, 'params': seed.params, 'cookies': seed.cookies}
    config.update({
        'files': getattr(seed, 'files') if hasattr(seed, 'files') else None,
        'json': getattr(seed, 'json') if hasattr(seed, 'json') else None,
        'auth': getattr(seed, 'auth') if hasattr(seed, 'auth') else None,
        'hooks': getattr(seed, 'hooks') if hasattr(seed, 'hooks') else None,
    })
    return config


def send_config(seed, default_timeout):
    return {
        'timeout': getattr(seed, 'timeout') if hasattr(seed, 'timeout') else default_timeout,
        'verify': getattr(seed, 'verify') if hasattr(seed, 'verify') else True,
        'stream': getattr(seed, 'stream') if hasattr(seed, 'stream') else None,
        'cert': getattr(seed, 'cert') if hasattr(seed, 'cert') else None,
        'allow_redirects': getattr(seed, 'allow_redirects') if hasattr(seed, 'allow_redirects') else True,
        'proxies': getattr(seed, 'proxies') if hasattr(seed, 'proxies') else None
    }


def log_response(send_func):
    def handler(*args, **kwargs):
        ctime = time.time()
        resp = send_func(*args, **kwargs)
        respond_time = int((time.time() - ctime) * 1000)
        info = f'Response[{resp.status_code}] {resp.reason}, {respond_time}ms'
        Logger.instance().info(info)
        return resp

    return handler


def configured(request_func):
    def handler(self, **kwargs):
        seed = kwargs.get('seed')
        _req_config = request_config(seed)
        _send_config = send_config(seed, self.default_timeout)
        request = self.session.prepare_request(Request(**_req_config))
        Logger.instance().info(f'{request.method} {request.url}')
        return request_func(self, **dict(
            request = request,
            send_config = _send_config
        ))

    return handler


UserAgentPool = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
]
