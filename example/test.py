from genius_lite.core.genius_lite import GeniusLite

class TestSpider(GeniusLite):
    spider_name = 'TestSpider'

    def start(self):
        yield self.request(
            url='https://www.futbin.org/futbin/api/getFilteredPlayers',
            parser=self.parse,
            params={'page': 1, 'league': 19}
        )

    def parse(self, response):
        self.logger.debug(response.json())


if __name__ == '__main__':
    spider = TestSpider()
    spider.run()
