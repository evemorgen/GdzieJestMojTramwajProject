import json

from tornado.web import RequestHandler
from tornado.gen import coroutine


class TTworker(RequestHandler):
    def initialize(self, tt_worker):
        self.timetable_worker = tt_worker

    @coroutine
    def post(self, method):
        params = json.loads(self.request.body.decode('utf-8'))
        if method == 'force_update':
            self.timetable_worker.force_update = True
            yield self.timetable_worker.run()
            self.write({'status': 'OK'})
        elif method == 'get_status':
            if 'number' in params:
                ret = self.timetable_worker.get_status(number=params['number'])
            else:
                ret = self.timetable_worker.get_status()
            self.write({'status': ret})
