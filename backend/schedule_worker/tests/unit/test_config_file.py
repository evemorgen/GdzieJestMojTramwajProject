import json

from unittest import main, TestCase
from unittest.mock import patch, mock_open


class ConfigFileTest(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_load_json(self):
        with open('conf/config.json') as plik:
            json.load(plik)
