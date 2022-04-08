from genius_lite.core.genius_lite import GeniusLite


class TestSpider(GeniusLite):

    def start_requests(self):
        for i in range(2):
            yield self.crawl(
                url='https://www.baidu.com',
                parser=self.parse,
                params={'foo': i},
                timeout=3,
            )

    def parse(self, response):
        for i in range(3):
            yield self.crawl(
                url='https://www.baidu.com',
                parser=self.parse2,
                params={'foo': i},
                timeout=3,
            )

    def parse2(self, response):
        # self.logger.debug(response.payload)
        pass


if __name__ == '__main__':
    spider = TestSpider()
    spider.run()
