import logging

import yaml

from .generic import Singleton


class Config(metaclass=Singleton):

    def __init__(self, defaults=None):
        self.file = None
        self.defaults = defaults
        self.cfg = {} if defaults is None else defaults

    def dump(self):
        return yaml.dump(self.cfg, indent=2)

    def load(self, filename, override={}):
        self.file = filename
        self.cfg = {}
        try:
            logging.info('Read configuration from file %s', filename)
            with open(filename, 'r') as yf:
                loaded = yaml.load(yf.read())

            self.populate_dict(loaded)
        except:
            logging.exception("Config: load %s error", self.file)
            return -1

        for key, val in override.items():
            self.set(key, val)

        return True

    def populate_dict(self, data):
        for key, val in data.items():
            self.cfg[key] = val

    def __set(self, key, value, overwrite=False):
        dict_to_set = self.cfg
        current_path = []
        key_split = key.split('.')

        for sgm in key_split[:-1]:
            current_path.append(sgm)

            if sgm in dict_to_set:
                if not isinstance(dict_to_set[sgm], dict):
                    raise KeyError('Key "{}" exists and is not a dict'.join('.'.join(current_path)))

            dict_to_set.setdefault(sgm, {})
            dict_to_set = dict_to_set[sgm]

        if overwrite:
            dict_to_set[key_split[-1]] = value
        else:
            dict_to_set.setdefault(key_split[-1], value)

    def set(self, key, value):
        self.__set(key, value, True)

    def setdefault(self, key, value):
        self.__set(key, value, False)

    def get(self, key, default=None):
        return self.cfg.get(key, default)

    def __getitem__(self, key):
        return self.cfg.__getitem__(key)

    def __contains__(self, key):
        return key in self.cfg

    def __iter__(self):
        return self.cfg.__iter__()
