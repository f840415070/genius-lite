# genius_lite
> 基于 Python requests 库封装的轻量爬虫系统

## 安装
`pip install genius_lite`

## 使用
```python
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
```

### start_requests
所有爬虫请求的入口，爬虫子类必须重写该方法以生成请求种子
```python
from genius_lite import GeniusLite

class MySpider(GeniusLite):

    def start_requests(self):
        yield self.crawl(url='https://www.google.com', parser=self.parse_func)
    
    def parse_func(self, response):
        print(response.text)
```

### self.crawl
通过 yield 该方法生成爬虫请求种子，部分参数可查看 requests 文档 - https://docs.python-requests.org/en/latest/api/

- url: 请求地址
- parser: 响应解析函数，参数为 response 对象
- method: (default='GET') 请求方法
- params: (optional) 查询参数
- data: (optional) POST 请求参数
- headers: (optional) 请求头
- payload: (optional) 携带到响应解析函数的数据，通过 response.payload 形式读取
- encoding: (optional) response 编码设置
- unique: (default=True) 设置该请求是否唯一，设为 False 时将根据 url、method、params、data 内容进行去重
- kwargs: (optional) 支持的关键字参数如下：
    cookies, files, json, auth, hooks, timeout, verify, stream, cert, allow_redirects, proxies

### response
参考 [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response)


### GeniusLite config
```python
from genius_lite import GeniusLite

class MySpider(GeniusLite):
    spider_name = 'MySpider'
    spider_config = {'timeout': 15}
    log_config = {'output': '/absolute/path'}

    ...
```

#### spider_name
爬虫命名，不设置则默认为运行的爬虫子类名

#### spider_config
    name       | type              | default
    ————————————————————————————————————————————
    timeout    | num or (num, num) | 10
 
 爬虫全局设置
 
#### log_config
    name       | type              | default
    ————————————————————————————————————————————
    enable     | bool              | False
    level      | str               | 'DEBUG'
    output     | str               | None

log 配置
