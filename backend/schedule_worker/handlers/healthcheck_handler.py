import random
import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine


class HealthCheck(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    @coroutine
    def post(self):
        res = {
            'status': 'OK',
            'number': random.randint(0, 9)
        }
        logging.info("Healthcheck trigerred, sending back %s", res)
        self.write(res)

    def options(self):
        self.set_status(204)
        self.finish()
