import json
import unittest
from unittest.mock import MagicMock, patch

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from handlers import HealthCheck


class TestHealthcheckHandler(AsyncHTTPTestCase):
    def setUp(self):
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
            (r"/healthcheck", HealthCheck),
        ])

    def test_response(self):
        res = self.fetch(r'/healthcheck', method='POST', body="{}")
        body = json.loads(res.body.decode('utf-8'))
        self.assertEqual(res.code, 200)
        self.assertEqual(body['status'], 'OK')
        self.assertTrue(isinstance(body['number'], int))
