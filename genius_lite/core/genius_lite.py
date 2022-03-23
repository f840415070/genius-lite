from time import time

class GeniusLite:
    spider_name = ''

    def __init__(self):
        if not self.spider_name.strip():
            self.spider_name = f'spider{int(round(time() * 1000))}'
