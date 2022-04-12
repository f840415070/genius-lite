# genius_lite
> 基于 Python requests 库的轻量爬虫系统

## 安装
`pip install genius_lite`

## 使用
```python
from genius_lite import GeniusLite

class MySpider(GeniusLite):
    spider_name = 'MySpider' # 爬虫名称，不设置默认爬虫类名
    spider_config = {'timeout': 15}
    log_config = {'output': '/absolute/path'}
    
    def start_requests(self):
        pages = [1, 2, 3, 4]
        for page in pages:
            yield self.crawl(
                'http://xxx/list',
                self.parse_list_page,
                params={'page': page}
            )

    def parse_list_page(self, response):
        print(response.text)
        ... # do something
        detail_urls = [...]
        for url in detail_urls:
            yield self.crawl(
                url,
                self.parse_detail_page,
                payload='some data'
            )

    def parse_detail_page(self, response):
        print(response.payload) # output: some data
        ... # do something


my_spider = MySpider()
my_spider.run()
```

### spider_config
    name       | type              | default
    ————————————————————————————————————————————
    timeout    | num or (num, num) | 10
    
### log_config
    name       | type              | default
    ————————————————————————————————————————————
    enable     | bool              | False
    level      | str               | 'DEBUG'
    output     | str               | None

### start_requests
所有爬虫请求的入口，爬虫子类都要重写该方法
```python
def start_requests(self):
    yield self.crawl(url='http://...', parser=self.parse_func)

def parse_func(self, response):
    print(response.text)
```

### self.crawl
设置即将被爬取的爬虫种子配置
```python
def crawl(self, url, parser, method='GET', data=None, params=None,
          headers=None, payload=None, encoding=None, **kwargs):
    """设置即将被爬取的爬虫种子配置

    :param url: URL for the new :class:`Request` object.
    :param parser: a callback function to handle response
    :param method: (optional) method for the new :class:`Request` object,
        default 'GET'
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param params: (optional) Dictionary or bytes to be sent in the query
        string for the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the
        :class:`Request`.
    :param payload: (optional) the payload data to the parser function
    :param encoding: (optional) set response encoding
    
    :param kwargs:
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``. When set to
            ``False``, requests will accept any TLS certificate presented by
            the server, and will ignore hostname mismatches and/or expired
            certificates, which will make your application vulnerable to
            man-in-the-middle (MitM) attacks. Setting verify to ``False`` 
            may be useful during local development or testing.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
    :return: Seed
    """
```

### response
`requests` 库的 `Response` 对象，包含 `crawl` 方法设置的 `payload` 属性
