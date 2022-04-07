from genius_lite.core.genius_lite import GeniusLite


class TestSpider(GeniusLite):

    def start_requests(self):
        yield self.crawl(
            url='https://www.google.com',
            parser=self.parse,
            timeout=3,
        )

    def parse(self, response):
        for i in [3, 4]:
            yield self.crawl(
                url='',
                parser=self.parse2,
                params={'pageNum': 1, 'pageSize': i},
                data={'foo': 'bar', 'baz': 123, 'bar': True},
                headers={
                    'Authorization': '19b4dae1-3b1d-4d9d-976e-c7d10e787bcc'
                },
                payload=i
            )

    def parse2(self, response):
        # self.logger.debug(response.payload)
        pass


if __name__ == '__main__':
    spider = TestSpider()
    spider.run()
