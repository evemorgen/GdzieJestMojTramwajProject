import json
import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine

from db import RealDb


class RealDataHandler(RequestHandler):

    def initialize(self):
        self.db = RealDb()
        self.db.get_all()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST')

    @coroutine
    def post(self):
        params = json.loads(self.request.body.decode('utf-8'))
        logging.info('putting new point (%s, %s) to line %s', params['lat'], params['lon'], params['line'])
        self.db.insert_point(params['id'], params['lat'], params['lon'], params['line'], params['ts'])
        self.write("OK")

    @coroutine
    def get(self):
        mes_id = self.get_argument('id')
        lat = self.get_argument('lat')
        lon = self.get_argument('lon')
        line = self.get_argument('line')
        timestamp = self.get_argument('ts')
        logging.info('putting new point (%s, %s) to line %s', lat, lon, line)
        self.db.insert_point(mes_id, lat, lon, line, timestamp)
        self.write("OK")
