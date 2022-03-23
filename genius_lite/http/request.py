from requests import Session, Request
from genius_lite.utils.logger import Logger

class HttpRequest:
    def __init__(self):
        self.logger = Logger.instance()
        self.session = Session()

    def request(self):
        ...

    def execute(self):
        ...
