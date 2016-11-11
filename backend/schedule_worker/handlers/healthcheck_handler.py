import random
import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine


class HealthCheck(RequestHandler):

    @coroutine
    def post(self):
        res = {
            'status': 'OK',
            'number': random.randint(0, 9)
        }
        logging.info("Healthcheck trigerred, sending back %s", res)
        self.write(res)
