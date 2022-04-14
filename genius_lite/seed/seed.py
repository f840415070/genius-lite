from requests import Request

from genius_lite.utils.tool import md5, obj_to_str, str_sort


class Seed:
    def __init__(self, url=None, parser=None, method=None, data=None, params=None, headers=None, payload=None,
                 encoding=None, cookies=None, files=None, json=None, auth=None, hooks=None, timeout=None, verify=None,
                 stream=None, cert=None, allow_redirects=None, proxies=None, unique=None):
        self.id = self.create_id(url, method, params, data)
        self.url = url
        self.parser = parser
        self.method = method
        self.params = params
        self.data = data
        self.payload = payload
        self.headers = headers
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
        self.unique = unique

        self.time = None

    def __str__(self):
        dict_values = [(key, value) for key, value in self.__dict__.items() if value is not None]
        seed_props = ', '.join([self._str_value(key, value) for key, value in dict_values])
        return 'Seed(%s)' % seed_props

    def _str_value(self, key, value):
        return "%s='%s'" % (key, value) if isinstance(value, str) else '%s=%s' % (key, value)

    def create_id(self, url, method, params, data):
        data_str = url + method
        if params:
            data_str += obj_to_str(params)
        if data:
            data_str += obj_to_str(data)
        return md5(str_sort(data_str))

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
