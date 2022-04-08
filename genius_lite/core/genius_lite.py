import traceback
from abc import ABCMeta, abstractmethod

from genius_lite.http.request import HttpRequest
from genius_lite.http.user_agent import get_ua
from genius_lite.seed.seed import Seed
from genius_lite.seed.store import Store
from genius_lite.log.logger import Logger


class GeniusLite(metaclass=ABCMeta):
    """爬虫基类

    Basic Usage::

    >>> from genius_lite import GeniusLite

    >>> class MySpider(GeniusLite):
    >>>     spider_name = 'MySpider' # 爬虫名称，不设置默认爬虫类名
    >>>     spider_config = {'timeout': 15}
    >>>     log_config = {'output': '/absolute/path'}

    >>>     def start_requests(self):
    >>>         pages = [1, 2, 3, 4]
    >>>         for page in pages:
    >>>             yield self.crawl(
    >>>                 'http://xxx/list',
    >>>                 self.parse_list_page,
    >>>                 params={'page': page}
    >>>             )

    >>>     def parse_list_page(self, response):
    >>>         print(response.text)
    >>>         ... # do something
    >>>         detail_urls = [...]
    >>>         for url in detail_urls:
    >>>             yield self.crawl(
    >>>                 url,
    >>>                 self.parse_detail_page,
    >>>                 payload='some data'
    >>>             )

    >>>     def parse_detail_page(self, response):
    >>>         print(response.payload)
    >>>         ... # do something


    >>> my_spider = MySpider()
    >>> my_spider.run()

    """
    spider_name = ''
    spider_config = {}
    log_config = {}

    def __init__(self):
        if not self.spider_name.strip():
            self.spider_name = self.__class__.__name__
        self.logger = Logger.instance(self.spider_name, **self.log_config)
        self._store = Store()
        self.request = HttpRequest()
        self.default_timeout = self.spider_config.get('timeout') or 10

    @abstractmethod
    def start_requests(self):
        """所有爬虫请求的入口，爬虫子类都要重写该方法

        Basic Usage::

        >>> def start_requests(self):
        >>>     yield self.crawl(url='http://...', parser=self.parse_func)
        >>>
        >>> def parse_func(self, response):
        >>>     print(response.text)

        """
        pass

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
        :return: Seed
        """
        kwargs.update(dict(
            url=url, parser=parser, method=method, data=data, params=params,
            headers=headers, payload=payload, encoding=encoding
        ))
        self._prepare(kwargs)
        return Seed(**kwargs)

    def _prepare(self, kwargs):
        if hasattr(kwargs.get('parser'), '__call__'):
            kwargs['parser'] = kwargs['parser'].__name__
        self._validate_parser(kwargs.get('parser'))

        if not kwargs.get('headers'):
            kwargs['headers'] = {}
        if isinstance(kwargs['headers'], dict):
            kwargs['headers'].setdefault('User-Agent', get_ua())
        else:
            raise TypeError('headers must be a dict!')
        kwargs.setdefault('timeout', self.default_timeout)
        kwargs.setdefault('verify', True)
        kwargs.setdefault('allow_redirects', True)

    def _validate_parser(self, parser):
        if isinstance(parser, str) and hasattr(self, parser):
            return
        raise NotImplementedError('self.%s() not implemented!' % parser)

    def _run_once(self):
        seed = self._store.fetch()
        if seed is None:
            return
        if not isinstance(seed, Seed):
            self.logger.warning(
                'Invalid Seed. '
                'Perhaps you forgot to use `yield self.crawl(...)`'
            )
            return
        response = self.request.parse(seed)
        if not response:
            return
        response.payload = seed.payload
        try:
            seeds = getattr(self, seed.parser)(response)
            self._store.put(seeds)
        except:
            self.logger.error('\n%s' % traceback.format_exc())

    def run(self):
        start_seeds = self.start_requests()
        self._store.put(start_seeds)
        while self._store.not_empty:
            self._run_once()
