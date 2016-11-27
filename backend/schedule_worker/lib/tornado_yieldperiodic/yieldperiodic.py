"""Class for better periodic call handling"""
import tornado
import tornado.gen
import logging

class YieldPeriodicCallback(object):
    """Class for better periodic call"""

    def __init__(self, callback, callback_time, io_loop=None, faststart=False):
        """Init method it can be used like tornado periodic callback, but it has
        extra paramtetr
        :param faststart:  if true callback will be run after application start
        """
        self.callback = callback
        if callback_time <= 0:
            raise ValueError("Periodic callback must have a positive callback_time")
        self.callback_time = callback_time
        self.io_loop = io_loop or tornado.ioloop.IOLoop.current()
        self._running = False
        self._timeout = None

        if faststart:
            self._running = True
            self._next_timeout = self.io_loop.time()
            self._timeout = self.io_loop.add_timeout(self._next_timeout, self._run)

    def start(self):
        """Starts the timer"""
        if self._running:
            return
        self._running = True
        self._next_timeout = self.io_loop.time()
        self._schedule_next()

    def stop(self):
        """Stops the timer"""
        self._running = False
        if self._timeout is not None:
            self.io_loop.remove_timeout(self._timeout)
            self._timeout = None

    @tornado.gen.coroutine
    def _run(self):
        """Run the run method and schedule next time"""
        if not self._running:
            return
        try:
            yield self.callback()
        except Exception: # pylint: disable=W0703
            logging.error("Error in periodic callback", exc_info=True)
        self._schedule_next()

    def _schedule_next(self):
        """Schedule next callback method"""
        if self._running:
            current_time = self.io_loop.time()
            while self._next_timeout <= current_time:
                self._next_timeout += self.callback_time / 1000.0
            self._timeout = self.io_loop.add_timeout(self._next_timeout, self._run)



