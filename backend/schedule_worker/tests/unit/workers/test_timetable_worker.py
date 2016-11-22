import datetime

from unittest.mock import patch, call, mock_open, MagicMock
from tornado.testing import AsyncTestCase, gen_test
from tornado.concurrent import Future

from workers import TimetableWorker


def futurized(result):
    future = Future()
    if isinstance(result, Exception):
        future.set_exception(result)
    else:
        future.set_result(result)
    return future


class TestTTWorker(AsyncTestCase):
    def setUp(self):
        super().setUp()
        self.environ_dict = {
            'TRAM_ROOT': 'mock_value'
        }
        self.config_dict = {
            'get_db_link': 'mock_mpk_link',
            'mpk_headers': {
                'header1': 'mock_header_1',
                'header2': 'mock_header_2',
            },
            'get_point_data_link': 'mock_data_link',
            'ttworker_refresh_period': 100
        }
        patch.dict('workers.timetable_worker.os.environ', self.environ_dict).start()
        self.os_rename = patch('workers.timetable_worker.os.rename').start()
        self.mock_config = patch('workers.timetable_worker.Config', return_value=self.config_dict).start()
        self.mock_mpk_db = patch('workers.timetable_worker.MpkDb').start()
        self.mock_przystanki_db = patch('workers.timetable_worker.PrzystankiDb').start()
        self.mock_http = patch('workers.timetable_worker.AsyncHTTPClient').start()
        self.mock_ypc = patch('workers.timetable_worker.YieldPeriodicCallback').start()
        self.tt_worker = TimetableWorker()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_constructor_all_default(self):
        self.assertEqual(self.tt_worker.number, 1)
        self.assertEqual(self.tt_worker.last_db_update, None)
        self.assertEqual(self.tt_worker.db_file, self.environ_dict['TRAM_ROOT'] + '/data/')
        self.assertEqual(self.tt_worker.config, self.config_dict)
        self.assertEqual(self.tt_worker.force_update, False)
        self.assertEqual(self.tt_worker.status[1][0], 'not running')
        self.assertTrue(isinstance(self.tt_worker.status[1][1], str))
        self.assertEqual(self.tt_worker.status[0][0], 'TTworker initialised')
        self.assertTrue(isinstance(self.tt_worker.status[0][1], str))
        self.assertEqual(self.tt_worker.mpk_link, self.config_dict['get_db_link'])
        self.assertEqual(self.tt_worker.mpk_point_data, self.config_dict['get_point_data_link'])
        self.assertEqual(self.tt_worker.headers, self.config_dict['mpk_headers'])

    def test_update_status(self):
        self.tt_worker.update_status('abba')
        self.assertEqual(self.tt_worker.status[0][0], 'abba')
        self.assertTrue(isinstance(self.tt_worker.status[0][1], str))

    def test_get_status_default_num(self):
        ret = self.tt_worker.get_status()
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0][0], 'get_status requested')
        self.assertTrue(isinstance(ret[0][1], str))

    def test_get_status_bigger_num(self):
        ret = self.tt_worker.get_status(3)
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret[0][0], 'get_status requested')
        self.assertTrue(isinstance(ret[0][1], str))

    @gen_test
    def test_get_new_db_first_run(self):
        res_string = '{"d": {"body": "mock_link_to_new_db"}}'
        res_stuff = MagicMock()
        res_stuff.body.decode.return_value = res_string
        baza_mock = MagicMock()
        baza_mock.body.return_value = 'abc'
        self.mock_http().fetch.return_value = futurized(baza_mock)
        self.m = mock_open()
        with patch('workers.timetable_worker.open', self.m, create=True):
            yield self.tt_worker.get_new_db(res_stuff)
        self.assertFalse(self.tt_worker.force_update)
        self.assertTrue(isinstance(self.tt_worker.last_db_update, datetime.datetime))
        self.m().write.assert_called_once_with(baza_mock.body)
        self.mock_http().fetch.assert_called_once_with({'body': 'mock_link_to_new_db'}, request_timeout=600)

    @gen_test
    def test_push_to_przystanki(self):
        mock_body_dict = {
            'pointId': 'mock_point_id',
            'variantId': 'mock_variant_id',
        }
        mock_res_dict = MagicMock()
        mock_res_dict.body.decode.return_value = '{"d": {"StopName": "mock_stop_name", "LineName": "mock_line_name","PointTime": [1,2,3], "Route": "mock_route"}}'
        mock_push = {
            'pointId': mock_body_dict['pointId'],
            'pointName': 'mock_stop_name',
            'variantId': mock_body_dict['variantId'],
            'lineName': 'mock_line_name',
            'pointTime': "[1, 2, 3]",
            'route': 'mock_route'
        }
        yield self.tt_worker.push_to_przystanki(mock_body_dict, mock_res_dict)
        self.mock_przystanki_db().insert.assert_called_once_with(mock_push)
