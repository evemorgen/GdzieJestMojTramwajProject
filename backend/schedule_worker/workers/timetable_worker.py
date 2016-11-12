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


class TimetableWorker(YieldPeriodicCallback):

    def __init__(self):
        self.number = 1
        self.last_db_update = None
        self.db_file = os.environ['TRAM_ROOT'] + '/data/'
        self.db = MpkDb()
        self.przystanki_db = PrzystankiDb()
        self.mpk_link = 'http://m.rozklady.mpk.krakow.pl/Services/data.asmx/GetDatabase'
        self.mpk_point_data = 'http://m.rozklady.mpk.krakow.pl/Services/data.asmx/GetPointData'
        self.force_update = False
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Content-Length': 0,
            'Host': 'm.rozklady.mpk.krakow.pl',
            'Connection': 'close'
        }
        self.httpclient = AsyncHTTPClient()
        YieldPeriodicCallback.__init__(self, self.run, 60000, faststart=True)
        self.status = [('not running', str(datetime.datetime.now()))]

    def update_status(self, message):
        self.status.insert(0, (message, str(datetime.datetime.now())))

    def get_status(self, number=1):
        return self.status[0:number]

    @coroutine
    def get_new_db(self, res):
        if self.force_update or\
           self.last_db_update is None or\
           datetime.datetime.now() - self.last_db_update > datetime.timedelta(minutes=5):
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
            self.update_status('done')
            os.rename(self.db_file + 'baza.zip', self.db_file + 'baza.ready.zip')
        else:
            logging.info("5 minutes didnt pass")

    @coroutine
    def push_to_przystanki(self, body, res):
        data = json.loads(res.body.decode('utf-8'))['d']
        print(data)
        to_push = {
            'pointId': body['pointId'],
            'pointName': data['StopName'],
            'variantId': body['variantId'],
            'lineName': data['LineName'],
            'pointTime': json.dumps(data['PointTime']),
            'ttl': 7
        }
        self.przystanki_db.insert(to_push)

    @coroutine
    def fill_przystanki_db(self, lines):
        for line in lines:
            logging.info('fetching line %s', line)
            line_points = self.db.get_line_points(line)
            print(line_points)
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
        yield self.fill_przystanki_db([62, 64])
        logging.info("running for %d time" % self.number)
        self.update_status('fetching info about db version')
        yield self.httpclient.fetch(self.mpk_link, self.get_new_db, method='POST', body=urllib.parse.urlencode({}), headers=self.headers)
        self.number += 1
