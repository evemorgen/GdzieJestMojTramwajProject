import os
import logging
import urllib
import json
import datetime
import sqlite3

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback


class TimetableWorker(YieldPeriodicCallback):

    def __init__(self):
        self.number = 1
        self.last_db_update = None
        self.db_file = os.environ['TRAM_ROOT'] + '/data/'
        self.mpk_link = 'http://m.rozklady.mpk.krakow.pl/Services/data.asmx/GetDatabase'
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

        db_connection = sqlite3.connect(self.db_file + 'baza.ready.zip')
        self.cursor = db_connection.cursor()
        self.cursor.execute('select name from lines;')
        result = self.cursor.fetchall()
        db_connection.commit()
        logging.info(result)

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
    def run(self):
        logging.info("running for %d time" % self.number)
        self.update_status('fetching info about db version')
        yield self.httpclient.fetch(self.mpk_link, self.get_new_db, method='POST', body=urllib.parse.urlencode({}), headers=self.headers)
        self.number += 1
