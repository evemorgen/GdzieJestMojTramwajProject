import logging
import os
import json
import time

from tornado.gen import coroutine
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback

from utils import Config, Przystanki, TramwajFactory
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
        self.nowe_tramwaje = []
        self.factorio = TramwajFactory()
        YieldPeriodicCallback.__init__(self, self.run, 60000, faststart=True)
        logging.info('SpawnWorker initialised')

    def serialize_tram(self, tram):
        return {
            'line': tram.line,
            'velocity': tram.velocity,
            'state': tram.state,
            'last_stop': tram.last_stop,
            'next_stop': tram.next_stop,
            'position': {
                'x': tram.position['x'],
                'y': tram.position['y']
            },
            'distance_to_go': tram.distance_to_go,
            'last_update': tram.last_update
        }

    def get_json_tram(self, line):
        to_send = []
        for tram in self.tramwaje:
            if tram.line == line:
                to_send.append(self.serialize_tram(tram))
        return to_send

    def get_json_trams(self):
        to_send = []
        for tram in self.tramwaje:
            to_send.append(self.serialize_tram(tram))
        return to_send

    def get_new_json_trams(self):
        to_send = []
        for tram in self.nowe_tramwaje:
            to_send.append(self.serialize_tram(tram))
        self.nowe_tramwaje = []
        return to_send

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
                        logging.info('spawninig line: %s from %s', linia, petla)
                        tram = self.factorio.factory(linia, petla)
                        self.tramwaje.append(tram)
                        self.nowe_tramwaje.append(tram)
                        logging.info(self.tramwaje)
