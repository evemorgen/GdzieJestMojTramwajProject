import os
import sys
import logging

from tornado.web import Application
from tornado.ioloop import IOLoop

from utils import Config, logging_config
from workers import TimetableWorker
from handlers import HealthCheck, TTworker


def make_app():
    return Application([
        (r'/healthcheck', HealthCheck),
        (r'/mpk_db/(.*)', TTworker, {'tt_worker': tt_worker})
    ])

if __name__ == "__main__":
    os.environ['TRAM_ROOT'] = os.getcwd()
    logging_config()
    logging.info("starting app")
    tt_worker = TimetableWorker()
    config = Config()
    app = make_app()
    app.listen(sys.argv[1])
    IOLoop.current().start()
