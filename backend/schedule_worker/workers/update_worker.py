import logging
import os
import json
import time

from tornado.gen import coroutine
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback

class UpdateWorker(YieldPeriodicCallback):
    def __init__(self, trams_list):
        self.tramwaje = trams_list
        YieldPeriodicCallback.__init__(self, self.run, 5000, faststart=True)

    @coroutine
    def run(self):
        for tram in self.tramwaje:
            logging.info('tram %s between %s and %s with distance %s', tram.line, tram.last_stop['name'], tram.next_stop['name'], tram.distance_to_go)
            tram.calculate_distance()
