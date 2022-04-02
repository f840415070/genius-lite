import traceback
from abc import ABCMeta, abstractmethod
from typing import Generator

from genius_lite.http.request import HttpRequest
from genius_lite.seed.seed import Seed
from genius_lite.seed.seed_basket import SeedBasket
from genius_lite.utils.logger import Logger


class GeniusLite(metaclass=ABCMeta):
    spider_name = ''
    spider_config = {}

    def __init__(self):
        if not self.spider_name.strip():
            self.spider_name = self.__class__.__name__
        self.__seed_basket = SeedBasket()
        self.logger = Logger.instance(self.spider_name, **self.spider_config)
        self.http_request = HttpRequest(**self.spider_config)

    @abstractmethod
    def start_requests(self) -> Generator[Seed, None, None]:
        pass

    def make_seed(self, url, parser, method = 'GET', data = None,
                  params = None, headers = None, payload = None,
                  encoding = None, cookies = None, **kwargs):
        _parser = parser
        if hasattr(parser, '__call__'):
            _parser = parser.__name__
        kwargs.update(dict(method=method, data=data, params=params, cookies=cookies,
                           headers=headers, payload=payload, encoding=encoding))
        return Seed(url=url, parser=_parser, **kwargs)

    def __run_once(self):
        seed = self.__seed_basket.seed()
        if not seed:
            return
        resp = self.http_request.execute(seed)
        if not resp:
            return
        try:
            resp.payload = seed.payload
            seeds = getattr(self, seed.parser)(resp)
            self.__seed_basket.put(seeds)
        except:
            self.logger.error(f'\n{traceback.format_exc()}')

    def run(self):
        start_seeds = self.start_requests()
        self.__seed_basket.put(start_seeds)
        while self.__seed_basket.has_seeds:
            self.__run_once()
