import random
import logging
import time

from geopy.distance import vincenty

from db import MpkDb
from utils import Przystanki


class Tramwaj:
    def __init__(self, line, route, terminal):
        self.przystanki = Przystanki()
        self.line = line
        self.route = route
        self.normal_velocity = random.randint(19, 27)
        self.velocity = self.normal_velocity  # km/h
        self.stop_time = 10
        self.state = "I'm going to the next stop"
        self.delete_me = False
        self.last_stop = {
            'name': terminal,
            'x': float(self.przystanki.wszystkie[terminal]['x']),
            'y': float(self.przystanki.wszystkie[terminal]['y'])
        }
        self.next_stop = {
            'name': None,
            'x': 0,
            'y': 0,
        }
        self.calculate_next_stop()
        self.position = {
            'x': self.przystanki.petle[self.last_stop['name']]['x'],
            'y': self.przystanki.petle[self.last_stop['name']]['y']
        }
        self.distance_to_go = 0
        self.last_update = time.time()
        #self.last_updated = time.time()
        self.calculate_distance()

    def __repr__(self):
        string = '([{}] v: {}, pos: ({}, {}), last_stop: {})'.format(self.line, self.velocity, self.position['x'], self.position['y'], self.last_stop)
        return string

    def calculate_position(self):
        a = (self.next_stop['y'] - self.last_stop['y']) / (self.next_stop['x'] - self.last_stop['x'])
        b = self.last_stop['y'] - a * self.last_stop['x']
        x = self.last_stop['x']
        distance = vincenty((x, a * x + b), (self.next_stop['x'], self.next_stop['y'])).meters
        i = 0
        while(distance > self.distance_to_go) and self.distance_to_go > 5 and i < 1000:
            i += 1
            distance = vincenty((x, a * x + b), (self.next_stop['x'], self.next_stop['y'])).meters
            if x - self.next_stop['x'] < 0:
                x += 0.000050
            else:
                x -= 0.000050
        self.position['x'] = x
        self.position['y'] = a * x + b
        logging.info('x: %s, y: %s, distance: %s, distance to go: %s', x, a * x + b, distance, self.distance_to_go)

    def calculate_next_stop(self):
        if self.route.index(self.last_stop['name']) != len(self.route):
            next_stop_name = self.route[self.route.index(self.last_stop['name']) + 1]
            self.next_stop = {
                'name': next_stop_name,
                'x': float(self.przystanki.wszystkie[next_stop_name]['x']),
                'y': float(self.przystanki.wszystkie[next_stop_name]['y'])
            }

    def calculate_distance(self):
        if self.distance_to_go <= 0:
            if self.state == "Standing on stop":
                logging.info(time.time() - self.stop_to_time)
                logging.info(self.stop_time)
                if time.time() - self.stop_to_time > self.stop_time:
                    self.distance_to_go = self.przystanki.graph.get_edge_data(self.next_stop['name'], self.last_stop['name'])['odleglosc'] + self.distance_to_go
                    self.start()
            else:
                self.stop()
        else:
            self.distance_to_go = self.distance_to_go - (10 / 36) * self.velocity * (time.time() - self.last_update)
        self.calculate_position()
        self.last_update = time.time()

    def stop(self):
        logging.info('linia %s staje na przystanku', self.line)
        self.velocity = 0
        edge = self.przystanki.get_edge(self.last_stop['name'], self.next_stop['name'])
        if edge[0] == self.last_stop:
            queue = edge[2]['kolejka_L']
            try:
                queue.popleft()
            except IndexError:
                pass
            self.przystanki.set_queue(self.last_stop['name'], self.next_stop['name'], 'kolejka_L', queue)
        else:
            queue = edge[2]['kolejka_R']
            try:
                queue.popleft()
            except IndexError:
                pass
            self.przystanki.set_queue(self.last_stop['name'], self.next_stop['name'], 'kolejka_R', queue)
        self.last_stop = self.next_stop
        self.calculate_next_stop()
        edge = self.przystanki.get_edge(self.last_stop['name'], self.next_stop['name'])
        if edge[0] == self.last_stop:
            queue = edge[2]['kolejka_L']
            queue.append(self)
            self.przystanki.set_queue(self.last_stop['name'], self.next_stop['name'], 'kolejka_L', queue)
        else:
            queue = edge[2]['kolejka_R']
            queue.append(self)
            self.przystanki.set_queue(self.last_stop['name'], self.next_stop['name'], 'kolejka_R', queue)
        self.state = "Standing on stop"
        self.stop_to_time = time.time()
        logging.info(self.przystanki.get_edges(self.line))

    def start(self):
        logging.info('startuje')
        self.velocity = random.randint(19, 27)
        self.state = "I'm going to the next stop"

    def self_destruct(self):
        self.delete_me = True


class TramwajFactory:
    def __init__(self):
        self.mpk_db = MpkDb()

    def factory(self, line, terminal):
        variants = self.mpk_db.get_variants_for_line(line)
        for variant in variants:
            stops = self.mpk_db.get_stops_for_variant(variant)
            if stops[0] == terminal:
                tram = Tramwaj(line, stops, terminal)
                return tram
