import json

from tornado.web import RequestHandler
from tornado.gen import coroutine


class TTworker(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

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

    @coroutine
    def options(self, method):
        self.set_status(204)
        self.finish()
