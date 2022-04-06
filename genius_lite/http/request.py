import traceback
from time import time as current
from requests import Session, Request, exceptions
from genius_lite.log.logger import Logger


def responded(send_func):
    def handler(*args, **kwargs):
        start_time = current()
        resp = send_func(*args, **kwargs)
        end_time = int((current() - start_time) * 1000)
        info = f'Response[{resp.status_code}] {resp.reason}, {end_time}ms'
        Logger.instance().info(info)
        return resp

    return handler


def prepared(prepare_func):
    def handler(*args):
        request = prepare_func(*args)
        Logger.instance().info('%s %s' % (request.method, request.url))
        return request

    return handler


class HttpRequest:
    def __init__(self):
        self.logger = Logger.instance()
        self.session = Session()

    @responded
    def send(self, request, **kwargs):
        return self.session.send(request, **kwargs)

    @prepared
    def prepare_request(self, seed):
        return self.session.prepare_request(Request(**seed.prepare_req_kwargs))

    def request(self, seed):
        prepared_request = self.prepare_request(seed)
        return self.send(prepared_request, **seed.send_req_kwargs)

    def parse(self, seed):
        retry_count = 3
        while retry_count:
            try:
                response = self.request(seed)
                return response
            except (exceptions.Timeout, exceptions.ConnectTimeout, exceptions.ReadTimeout):
                retry_count -= 1
                self.logger.warning('Timeout')
            except:
                self.logger.error('\n%s' % traceback.format_exc())
                break
        return None
