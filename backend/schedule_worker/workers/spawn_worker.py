import logging
import os
import json
import time

from tornado.gen import coroutine
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback

from utils import Config, Przystanki, Tramwaj, TramwajFactory
from db import MpkDb, PrzystankiDb


class SpawnWorker(YieldPeriodicCallback):

    def __init__(self):
        self.number = 1
        self.db_file = os.environ['TRAM_ROOT'] + '/data/'
        self.config = Config()
        self.db = MpkDb()
        self.przystanki_db = PrzystankiDb()
        self.przystanki = Przystanki()
        self.tramwaje = []
        #self.factorio = TramwajFactory()
        #self.factorio.factory(18, "Krowodrza Górka")
        #YieldPeriodicCallback.__init__(self, self.run, 60000, faststart=True)
        logging.info('SpawnWorker initialised')

    @coroutine
    def run(self):
        logging.info('running for %s time', self.number)
        self.number += 1
        now_hour = time.strftime('%-H', time.localtime())
        now_minute = time.strftime("%M", time.localtime())
        petle = self.przystanki.petle
        for petla in petle:
            linie = petle[petla]['linie']
            for linia in linie:
                czas = self.przystanki_db.get_terminal_time(linia, petla)
                if czas is not None and czas != '{}':
                    czas = json.loads(czas)['02']
                    if now_minute in (czas.get(now_hour) if czas.get(now_hour) is not None else {}):
                        #self.tramwaje.append(Tramwaj(linia))
                        logging.info('spawninig line: %s from %s', linia, petla)
