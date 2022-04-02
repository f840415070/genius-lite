class Seed:
    kwargs_keys = [
        'timeout', 'verify', 'stream', 'cert', 'allow_redirects',
        'files', 'json', 'auth', 'hooks', 'proxies'
    ]

    def __init__(self, url, parser, method, data, params,
                 cookies, headers, payload, encoding, **kwargs):
        self.url = url
        self.parser = parser
        self.method = method
        self.data = data
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.payload = payload
        self.encoding = encoding
        for key in kwargs.keys():
            if key in self.kwargs_keys:
                setattr(self, key, kwargs[key])
