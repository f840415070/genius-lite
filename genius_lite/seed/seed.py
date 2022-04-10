from requests import Request
from genius_lite.utils.tool import md5, obj_to_str, str_sort


class Seed:
    def __init__(self, url=None, parser=None, method=None, data=None, params=None, headers=None, payload=None,
                 encoding=None, cookies=None, files=None, json=None, auth=None, hooks=None, timeout=None, verify=None,
                 stream=None, cert=None, allow_redirects=None, proxies=None):
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

        self.id = self.create_id()
        self.time = None

    def __str__(self):
        result = 'id[%s], url[%s], method[%s], parser[%s]' % (
            self.id,
            self.url,
            self.method,
            self.parser
        )
        if self.params:
            result += ', params[%s]' % obj_to_str(self.params)
        if self.data:
            result += ', data[%s]' % obj_to_str(self.data)
        if self.payload:
            result += ', payload[%s]' % obj_to_str(self.payload)

        return 'seed<%s>' % result

    def create_id(self):
        data = self.url + self.method
        if self.params:
            data += obj_to_str(self.params)
        if self.data:
            data += obj_to_str(self.data)
        return md5(str_sort(data))

    def create_request(self):
        return Request(
            url=self.url,
            method=self.method,
            data=self.data,
            params=self.params,
            headers=self.headers,
            cookies=self.cookies,
            files=self.files,
            json=self.json,
            auth=self.auth,
            hooks=self.hooks
        )

    @property
    def send_setting(self):
        return dict(
            timeout=self.timeout,
            verify=self.verify,
            stream=self.stream,
            cert=self.cert,
            allow_redirects=self.allow_redirects,
            proxies=self.proxies
        )
