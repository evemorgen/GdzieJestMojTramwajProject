import logging

from tornado.gen import coroutine
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback


class UpdateWorker(YieldPeriodicCallback):
    def __init__(self, trams_list, delay_factor_worker):
        self.tramwaje = trams_list
        self.delay_factor_worker = delay_factor_worker
        YieldPeriodicCallback.__init__(self, self.run, 3000, faststart=True)

    @coroutine
    def run(self):
        for tram in self.tramwaje:
            logging.info('tram %s between %s and %s with distance %s', tram.line, tram.last_stop['name'], tram.next_stop['name'], tram.distance_to_go)
            yield self.delay_factor_worker.calculate_factor(tram)
            tram.calculate_distance()
            if tram.delete_me is True:
                self.tramwaje.remove(tram)
