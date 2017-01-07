import random
import logging
import time

from db import MpkDb
from utils import Przystanki


class Tramwaj:
    def __init__(self, line, route, terminal):
        self.line = line
        self.route = route
        self.velocity = random.randint(19, 27)  # km/h
        self.state = "I'm going to the next stop"
        self.last_stop = terminal
        self.next_stop = None
        self.calculate_next_stop()
        self.przystanki = Przystanki()
        logging.info(self.przystanki.graph.edges(data=True))
        self.distance_to_go = 0
        self.last_updated = time.time()
        self.calculate_distance()

    def calculate_next_stop(self):
        if self.route.index(self.last_stop) != len(self.route) - 1:
            self.next_stop = self.route[self.route.index(self.last_stop) + 1]

    def calculate_distance(self):
        if self.distance_to_go <= 0:
            self.stop()
            self.distance_to_go = self.przystanki.graph.get_edge_data(self.next_stop, self.last_stop)['odleglosc'] + self.distance_to_go
            self.start()
        else:
            self.distance_to_go = self.distance_to_go - (10 / 36) * self.velocity * (time.time() - self.last_update)
        self.last_update = time.time()

    def stop(self):
        self.velocity = 0
        self.last_stop = self.next_stop
        self.calculate_next_stop()
        self.state = "Standing on stop"

    def start(self):
        self.velocity = random.randint(19, 27)
        self.state = "I'm going to the next stop"


class TramwajFactory:
    def __init__(self):
        self.mpk_db = MpkDb()

    def factory(self, line, terminal):
        variants = self.mpk_db.get_variants_for_line(line)
        for variant in variants:
            stops = self.mpk_db.get_stops_for_variant(variant)
            if stops[0] == terminal:
                tram = Tramwaj(line, stops, terminal)
                while True:
                    logging.info('between %s and %s with distance %s', tram.last_stop, tram.next_stop, tram.distance_to_go)
                    time.sleep(5)
                    tram.calculate_distance()
