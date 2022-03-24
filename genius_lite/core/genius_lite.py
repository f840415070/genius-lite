import traceback
from time import time
from collections.abc import Iterable
from genius_lite.seed.seed import Seed
from genius_lite.seed.seed_list import SeedList
from genius_lite.http.request import HttpRequest
from genius_lite.utils.logger import Logger

class GeniusLite:
    spider_name = ''
    spider_config = {}

    def __init__(self):
        if not self.spider_name.strip():
            self.spider_name = f'spider{int(round(time() * 1000))}'
        self.__seed_list = SeedList()
        self.logger = Logger.instance(self.spider_name, **self.spider_config)
        self.http_request = HttpRequest(**self.spider_config)

    def start(self):
        yield None

    def request(self, url, parser, method=None, data=None, params=None,
                cookies=None, headers=None, payload=None, encoding=None, **kwargs):
        _parser = parser
        if hasattr(parser, '__call__'):
            _parser = parser.__name__
        kwargs.update(dict(method=method, data=data, params=params, cookies=cookies,
                           headers=headers, payload=payload, encoding=encoding))
        return Seed(url=url, parser=_parser, **kwargs)

    def push_seeds(self, seeds):
        if not isinstance(seeds, Iterable):
            return
        for seed in seeds:
            if isinstance(seed, Seed):
                self.__seed_list.push(seed)

    def __run_once(self):
        seed = self.__seed_list.pop()
        if not isinstance(seed, Seed):
            self.logger.warning(f'Invalid seed: {seed}')
            return
        resp = self.http_request.execute(seed)
        if not resp:
            return
        try:
            results = getattr(self, seed.parser)(resp, seed.payload)
            self.push_seeds(results)
        except:
            self.logger.error(f'\n{traceback.format_exc()}')

    def run(self):
        self.push_seeds(self.start())
        while self.__seed_list.length:
            self.__run_once()
