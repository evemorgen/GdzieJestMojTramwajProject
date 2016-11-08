import os
import sys
import random
import logging
import coloredlogs

from tornado.web import RequestHandler
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.gen import coroutine

from utils.config import Config


class HealthCheck(RequestHandler):

    @coroutine
    def post(self):
        res = {
            'status': 'OK',
            'number': random.randint(0, 9)
        }
        logging.info("Healthcheck trigerred, sending back %s", res)
        self.write(res)


def make_app():
    return Application([
        (r'/healthcheck', HealthCheck)
    ])

if __name__ == "__main__":
    formatter = "[%(asctime)s %(funcName)s] %(message)s"
    os.environ['COLOREDLOGS_LOG_FORMAT'] = formatter
    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)
    app = make_app()
    app.listen(sys.argv[1])
    IOLoop.current().start()
