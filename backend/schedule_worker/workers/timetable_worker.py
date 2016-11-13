import os
import logging
import urllib
import json
import datetime
import functools

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback
from db import MpkDb, PrzystankiDb
from utils import Config


class TimetableWorker(YieldPeriodicCallback):

    def __init__(self):
        self.number = 1
        self.last_db_update = None
        self.db_file = os.environ['TRAM_ROOT'] + '/data/'
        self.config = Config()
        self.force_update = False
        self.status = [('not running', str(datetime.datetime.now()))]

        self.db = MpkDb()
        self.przystanki_db = PrzystankiDb()
        self.mpk_link = self.config['get_db_link']
        self.mpk_point_data = self.config['get_point_data_link']
        self.headers = self.config['mpk_headers']
        self.httpclient = AsyncHTTPClient()
        YieldPeriodicCallback.__init__(self, self.run, self.config['ttworker_refresh_period'] * 60000, faststart=True)
        self.update_status('TTworker initialised')

    def update_status(self, message):
        self.status.insert(0, (message, str(datetime.datetime.now())))

    def get_status(self, number=1):
        self.update_status('get_status requested')
        return self.status[0:number]

    @coroutine
    def get_new_db(self, res):
        self.update_status('fetching new db version')
        if self.force_update or\
           self.last_db_update is None or\
           datetime.datetime.now() - self.last_db_update > datetime.timedelta(hours=23):
            self.force_update = False
            self.last_db_update = datetime.datetime.now()
            zwrotka = json.loads(res.body.decode('utf-8'))
            logging.info("got %s from mpk", zwrotka)
            logging.info("downloading new db")
            self.update_status('downloading db')
            baza = yield self.httpclient.fetch(zwrotka['d'], request_timeout=600)
            self.update_status('saving db')
            with open(self.db_file + 'baza.zip', 'wb') as f:
                f.write(baza.body)
            logging.info("new db saved")
            self.update_status('db saved')
            os.rename(self.db_file + 'baza.zip', self.db_file + 'baza.ready.zip')
        else:
            logging.info("24 hours didnt pass")

    @coroutine
    def push_to_przystanki(self, body, res):
        data = json.loads(res.body.decode('utf-8'))['d']
        to_push = {
            'pointId': body['pointId'],
            'pointName': data['StopName'],
            'variantId': body['variantId'],
            'lineName': data['LineName'],
            'pointTime': json.dumps(data['PointTime']),
            'route': data['Route']
        }
        self.przystanki_db.insert(to_push)

    @coroutine
    def fill_przystanki_db(self, lines):
        self.update_status('filling przystanki db cache')
        self.przystanki_db.clear_table()
        for line in lines:
            logging.info('fetching line %s', line)
            self.update_status('fetching line %s' % line)
            line_points = self.db.get_line_points(line)
            for variant, points in line_points.items():
                for point in points:
                    body = {
                        "variantId": variant,
                        "pointId": point,
                        "lineName": line
                    }
                    cb = functools.partial(self.push_to_przystanki, body)
                    yield self.httpclient.fetch(self.mpk_point_data, cb, method='POST', body=json.dumps(body), headers=self.headers)

    @coroutine
    def run(self):
        logging.info("running for %d time" % self.number)
        self.update_status("running for %d time" % self.number)
        yield self.httpclient.fetch(self.mpk_link, self.get_new_db, method='POST', body=urllib.parse.urlencode({}), headers=self.headers)
        yield self.fill_przystanki_db(self.config.get('lines'))
        self.number += 1
