import json
import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine

from db import RealDb


class RealDataHandler(RequestHandler):

    def initialize(self):
        logging.info('heja')
        self.db = RealDb()
        self.db.get_all()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    @coroutine
    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
