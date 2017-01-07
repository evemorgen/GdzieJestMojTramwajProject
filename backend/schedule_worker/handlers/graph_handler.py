import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine

from utils import generate_graph


class GraphHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    @coroutine
    def post(self):
        logging.info('starting graph generation')
        generate_graph()
        res = {
            "status": "OK"
        }
        self.write(res)

    def options(self):
        self.set_status(204)
        self.finish()
