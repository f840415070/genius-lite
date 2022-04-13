import traceback
from time import time as current_time_stamp

from requests import Session, exceptions

from genius_lite.http.record import Record
from genius_lite.log.logger import Logger

TIMEOUT_EXCEPTIONS = (
    exceptions.Timeout,
    exceptions.ConnectTimeout,
    exceptions.ReadTimeout,
    exceptions.ConnectionError
)


def on_request(send_func):
    def handler(*args, **kwargs):
        logger = Logger.instance()
        request = args[1]
        seed = request.raw_seed
        logger.info('%s %s' % (request.method, request.url))

        start_time = current_time_stamp()
        response = send_func(*args, **kwargs)
        seed.time = int((current_time_stamp() - start_time) * 1000)

        msg = 'Response[%s] within %sms' % (response.status_code, seed.time)
        if response.status_code < 300:
            logger.info(msg)
        elif response.status_code < 400:
            logger.warning(msg)
        else:
            logger.error(msg)

        return response

    return handler


class HttpRequest:
    def __init__(self):
        self.logger = Logger.instance()
        self.session = Session()
        self.record = Record()
        self.retry_limit = 3

    @on_request
    def send(self, request, **kwargs):
        return self.session.send(request, **kwargs)

    def request(self, seed):
        times = 0
        prepared_request = self.session.prepare_request(seed.create_request())
        setattr(prepared_request, 'raw_seed', seed)
        while times <= self.retry_limit:
            try:
                response = self.send(prepared_request, **seed.send_setting)
                return response
            except TIMEOUT_EXCEPTIONS:
                self.logger.warning(
                    'Timeout(retry times: %s/%s) '
                    'when requesting %s' % (times, self.retry_limit, seed.url)
                )
                times += 1
                if times > 3:
                    self.logger.error(
                        'The maximum number of retries has been reached. '
                        'Drop request %s' % seed.url
                    )
        return None

    def parse(self, seed):
        if seed.unique and self.record.is_duplicate(seed.id):
            self.record.duplicate()
            self.logger.warning('Abandon the request with duplicate id %s' % seed.id)
            return None
        try:
            response = self.request(seed)
            if not response:
                self.record.failure()
            else:
                self.record.success(seed)
                if seed.encoding and isinstance(seed.encoding, str):
                    response.encoding = seed.encoding
            return response
        except:
            self.logger.error('\n%s' % traceback.format_exc())
            self.record.failure()
            return None

    def done(self):
        self.record.show()
