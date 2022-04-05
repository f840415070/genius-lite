import traceback
from abc import ABCMeta, abstractmethod

from genius_lite.http.request import HttpRequest
from genius_lite.http.user_agent import get_ua
from genius_lite.seed.seed import Seed
from genius_lite.seed.seed_basket import SeedBasket
from genius_lite.log.logger import Logger


class GeniusLite(metaclass=ABCMeta):
    """爬虫基类

    Basic Usage::

    >>> from genius_lite import GeniusLite
    >>>
    >>> class MySpider(GeniusLite):
    >>>     spider_name = 'MySpider'
    >>>     spider_config = {
    >>>         'timeout': 15,
    >>>         'log_level': 'INFO',
    >>>     }
    >>>     list_url = 'http://xxx'
    >>>     detail_url = 'http://xxx'
    >>>
    >>>     def start_requests(self):
    >>>         for i in range(5):
    >>>             yield self.crawl(
    >>>                 url=self.list_url + '?page=' + str(i + 1),
    >>>             )
    >>>
    >>>     def parse_list_page(self, response):
    >>>         print(response.text)
    >>>         yield self.crawl(
    >>>             url=self.detail_url,
    >>>             parser='parse_detail_page',
    >>>         )

    """
    spider_name = ''
    spider_config = {}

    def __init__(self):
        if not self.spider_name.strip():
            self.spider_name = self.__class__.__name__
        self._seed_basket = SeedBasket()
        self.logger = Logger.instance(self.spider_name, **self.spider_config)
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
        seed = self._seed_basket.seed()
        if not seed:
            return
        response = self.request.parse(seed)
        if not response:
            return
        try:
            response.payload = seed.payload
            seeds = getattr(self, seed.parser)(response)
            self._seed_basket.put(seeds)
        except:
            self.logger.error('\n%s' % traceback.format_exc())

    def run(self):
        start_seeds = self.start_requests()
        self._seed_basket.put(start_seeds)
        while self._seed_basket.has_seeds:
            self._run_once()
