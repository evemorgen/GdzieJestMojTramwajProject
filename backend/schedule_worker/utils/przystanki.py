import logging
import os
import json
import networkx as nx

from utils import Singleton


class Przystanki(metaclass=Singleton):

    def __init__(self, path=None):
        if path is None:
            self.path = os.environ['TRAM_ROOT'] + "/data/przystanki_0_159.json"
        else:
            self.path = path

        with open(self.path, 'r') as cfg_file:
            self.cfg = json.load(cfg_file)
        self.graph = nx.read_yaml(os.environ['TRAM_ROOT'] + "/data/graph.yaml")

        self.petle = {k: v for k, v in self.cfg.items() if self.cfg[k]['petla'] is True}
        self.skrzyzowania = {k: v for k, v in self.cfg.items() if self.cfg[k]['skrzyzowanie'] is True}
        self.przystanki = {k: v for k, v in self.cfg.items() if self.cfg[k]['przystanek'] is True}
        logging.info('Przystanki initialised')

    def get(self, item, default=None):
        return self.cfg.get(item, default)

    def set(self, key, value):
        self.cfg[key] = value

    def dump(self):
        with open(self.path, 'w') as out_file:
            json.dump(self.cfg, out_file, indent=4)

    def __getitem__(self, key):
        return self.cfg.__getitem__(key)

    def __contains__(self, key):
        return key in self.cfg
