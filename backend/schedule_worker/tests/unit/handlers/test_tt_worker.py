import json
import unittest
from unittest.mock import MagicMock, patch

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.concurrent import Future

from handlers import TTworker


def futurized(result):
    future = Future()
    if isinstance(result, Exception):
        future.set_exception(result)
    else:
        future.set_result(result)
    return future


class TestTTWorkerHandler(AsyncHTTPTestCase):
    def setUp(self):
        self.mock_tt_worker = MagicMock()
        super().setUp()
        self.app = MagicMock()
        self.request = MagicMock()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def get_new_ioloop(self):
        return IOLoop().instance()

    def get_app(self):
        return Application([
            (r'/mpk_db/(.*)', TTworker, {'tt_worker': self.mock_tt_worker}),
        ])

    def test_get_status_no_number(self):
        self.mock_tt_worker.get_status.return_value = 'MOCK OK'
        res = self.fetch(r'/mpk_db/get_status', method='POST', body='{}')
        body = json.loads(res.body.decode('utf-8'))
        self.assertEqual(res.code, 200)
        self.assertEqual(body['status'], 'MOCK OK')
        self.mock_tt_worker.get_status.assert_called_once_with()
        self.assertFalse(self.mock_tt_worker.force_update.called)

    def test_get_status_with_number(self):
        self.mock_tt_worker.get_status.return_value = 'MOCK OK'
        res = self.fetch(r'/mpk_db/get_status', method='POST', body='{"number":3}')
        body = json.loads(res.body.decode('utf-8'))
        self.assertEqual(res.code, 200)
        self.assertEqual(body['status'], 'MOCK OK')
        self.mock_tt_worker.get_status.assert_called_once_with(number=3)
        self.assertFalse(self.mock_tt_worker.force_update.called)

    def test_force_update(self):
        self.mock_tt_worker.get_status.return_value = 'MOCK OK'
        self.mock_tt_worker.run.return_value = futurized('None')
        res = self.fetch(r'/mpk_db/force_update', method='POST', body='{}')
        body = json.loads(res.body.decode('utf-8'))
        self.assertEqual(res.code, 200)
        self.assertEqual(body['status'], 'OK')
        self.mock_tt_worker.run.assert_called_once_with()
        self.assertEqual(self.mock_tt_worker.force_update, True)
        self.assertFalse(self.mock_tt_worker.get_status.called)
