import logging
import json

from tornado.web import RequestHandler
from tornado.gen import coroutine

from utils import generate_graph
from utils import Przystanki


class GraphHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    def initialize(self, spawn_worker):
        self.spawn_worker = spawn_worker

    @coroutine
    def post(self, method):
        logging.info('method: %s' % method)
        if method == 'generate_graph':
            generate_graph()
            res = {
                "status": "OK"
            }
            self.write(res)
        if method in ['get_all_stops', 'get_all_terminals', 'get_all_crossings']:
            przystanki = Przystanki()
            methods_data = {
                'get_all_stops': przystanki.przystanki,
                'get_all_terminals': przystanki.petle,
                'get_all_crossings': przystanki.skrzyzowania
            }
            res = {
                "data": methods_data[method],
                "status": "OK"
            }
            self.write(res)
        if method == 'get_graph_edges':
            przystanki = Przystanki()
            params = json.loads(self.request.body.decode('utf-8'))
            logging.info(params)
            res = {
                "data": przystanki.get_edges(line=params['line']),
                "status": "OK"
            }
            self.write(res)
        if method == 'get_trams':
            params = json.loads(self.request.body.decode('utf-8'))
            trams = self.spawn_worker.get_json_trams()
            logging.info(params)
            res = {
                "data": trams,
                "status": "OK"
            }
            self.write(res)

        if method == 'get_new_trams':
            params = json.loads(self.request.body.decode('utf-8'))
            trams = self.spawn_worker.get_new_json_trams()
            logging.info(params)
            res = {
                "data": trams,
                "status": "OK"
            }
            self.write(res)

    def options(self, method):
        self.set_status(204)
        self.finish()
