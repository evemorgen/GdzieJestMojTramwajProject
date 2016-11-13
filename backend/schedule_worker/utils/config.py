import logging
import os
import json
import pprint

from utils import Singleton


class Config(metaclass=Singleton):

    def __init__(self, path=None):
        if path is None:
            self.path = os.environ['TRAM_ROOT'] + "/conf/config.json"
        else:
            self.path = path

        with open(self.path, 'r') as cfg_file:
            self.cfg = json.load(cfg_file)
        logging.info('Config initialised')

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
