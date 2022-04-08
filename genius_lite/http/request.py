import traceback
from time import time as current
from requests import Session, Request, exceptions
from genius_lite.http.record import Record
from genius_lite.log.logger import Logger

TIMEOUT_EXCEPTIONS = (
    exceptions.Timeout,
    exceptions.ConnectTimeout,
    exceptions.ReadTimeout
)


def on_request(send_func):
    def handler(*args, **kwargs):
        logger = Logger.instance()

        request = args[1]
        logger.info('%s %s' % (request.method, request.url))

        start_time = current()
        response = send_func(*args, **kwargs)
        logger.info('Response[%s] %s, %sms' % (
            response.status_code,
            response.reason,
            int((current() - start_time) * 1000)
        ))

        return response

    return handler


class HttpRequest:
    def __init__(self):
        self.logger = Logger.instance()
        self.session = Session()
        self.record = Record()
        self.retry_limit_num = 3

    @on_request
    def send(self, request, **kwargs):
        return self.session.send(request, **kwargs)

    def prepare_request(self, seed):
        return self.session.prepare_request(Request(**seed.prepare_req_kwargs))

    def request(self, seed):
        retry_num = 0
        prepared_request = self.prepare_request(seed)
        while retry_num <= self.retry_limit_num:
            try:
                response = self.send(prepared_request, **seed.send_req_kwargs)
                return response
            except TIMEOUT_EXCEPTIONS:
                self.logger.warning(
                    'Timeout(retry times: %s/%s) '
                    'when requesting %s' % (retry_num, self.retry_limit_num, seed.url)
                )
                retry_num += 1
                if retry_num > 3:
                    self.logger.error(
                        'The maximum number of retries has been reached. '
                        'Drop request %s' % seed.url
                    )
        return None

    def parse(self, seed):
        if self.record.is_duplicate(seed.id):
            self.logger.info('Duplicate(id=%s) %s' % (seed.id, seed.url))
            self.record.duplicate()
            return None
        try:
            response = self.request(seed)
            if not response:
                self.record.failure()
            else:
                self.record.success(seed.id)
            return response
        except:
            self.logger.error('\n%s' % traceback.format_exc())
            self.record.failure()
            return None

    def all_tasks_done(self):
        self.record.show()
