import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine

from utils import generate_graph
from utils import Przystanki


class GraphHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    @coroutine
    def post(self, method):
        if method == 'generate_graph':
            generate_graph()
            res = {
                "status": "OK"
            }
            self.write(res)
        if method == 'get_all_stops':
            przystanki = Przystanki()
            res = {
                "data": przystanki.przystanki,
                "status": "OK"
            }
            self.write(res)

    def options(self):
        self.set_status(204)
        self.finish()
