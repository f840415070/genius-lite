import traceback
from abc import ABCMeta, abstractmethod

from genius_lite.http.request import HttpRequest
from genius_lite.http.user_agent import get_ua
from genius_lite.log.logger import Logger
from genius_lite.seed.seed import Seed
from genius_lite.seed.store import Store


class GeniusLite(metaclass=ABCMeta):
    """爬虫基类

    Basic Usage::

        from genius_lite import GeniusLite

        class MySpider(GeniusLite):

            def start_requests(self):
                yield self.crawl('https://www.google.com', self.parse_google_page)

            def parse_google_page(self, response):
                print(response.text)
                detail_urls = [...]
                for url in detail_urls:
                    yield self.crawl(url, self.parse_detail_page)

            def parse_detail_page(self, response):
                ...

        if __name__ == '__main__':
            my_spider = MySpider()
            my_spider.run()

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
        """所有爬虫请求的入口，爬虫子类必须重写该方法以生成请求种子

        Basic Usage::

            def start_requests(self):
                yield self.crawl(url='https://www.google.com', parser=self.parse_func)

            def parse_func(self, response):
                print(response.text)

        """
        pass

    def crawl(self, url, parser, method='GET', data=None, params=None,
              headers=None, payload=None, encoding=None, unique=True, **kwargs):
        """通过 yield 该方法生成爬虫请求种子，部分参数可查看 [requests](https://docs.python-requests.org/en/latest/api/#main-interface) 文档

        :param url: 请求地址
        :param parser: 响应解析函数，参数为 response 对象
        :param method: (default='GET') 请求方法
        :param params: (optional) 查询参数
        :param data: (optional) POST 请求参数
        :param headers: (optional) 请求头
        :param payload: (optional) 携带到响应解析函数的数据，通过 response.payload 形式读取
        :param encoding: (optional) response 编码设置
        :param unique: (default=True) 设置该请求是否唯一，设为 True 时将根据 url、method、params、data 内容过滤相同请求
        :param kwargs: (optional) 支持的关键字参数如下 cookies, files, json, auth, hooks, timeout, verify, stream, cert,
                                    allow_redirects, proxies

        :return: Seed
        """
        kwargs.update(dict(
            url=url, parser=parser, method=method, data=data, params=params,
            headers=headers, payload=payload, encoding=encoding, unique=unique
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
        if not isinstance(seed, Seed):
            return
        self.logger.info('Fetch %s' % seed)

        response = self.request.parse(seed)
        if not response:
            return
        setattr(response, 'payload', seed.payload)
        setattr(response, 'raw_seed', seed)
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
        self.request.done()
