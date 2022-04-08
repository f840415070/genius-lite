import hashlib


def md5(content):
    return hashlib.md5(content.encode()).hexdigest()[8:24]


class Seed:
    def __init__(self, url=None, parser=None, method=None, data=None, params=None, headers=None, payload=None,
                 encoding=None, cookies=None, files=None, json=None, auth=None, hooks=None, timeout=None, verify=None,
                 stream=None, cert=None, allow_redirects=None, proxies=None):
        self.id = self.md5(url)
        self.url = url
        self.parser = parser
        self.method = method
        self.data = data
        self.params = params
        self.headers = headers
        self.payload = payload
        self.encoding = encoding
        self.cookies = cookies
        self.files = files
        self.json = json
        self.auth = auth
        self.hooks = hooks
        self.timeout = timeout
        self.verify = verify
        self.stream = stream
        self.cert = cert
        self.allow_redirects = allow_redirects
        self.proxies = proxies

    def md5(self, target):
        return hashlib.md5(str(target).encode()).hexdigest()[8:24]

    @property
    def prepare_req_kwargs(self):
        return {
            'url': self.url, 'method': self.method, 'data': self.data, 'params': self.params, 'headers': self.headers,
            'cookies': self.cookies, 'files': self.files, 'json': self.json, 'auth': self.auth, 'hooks': self.hooks
        }

    @property
    def send_req_kwargs(self):
        return {
            'timeout': self.timeout, 'verify': self.verify, 'stream': self.stream,
            'cert': self.cert, 'allow_redirects': self.allow_redirects, 'proxies': self.proxies
        }
