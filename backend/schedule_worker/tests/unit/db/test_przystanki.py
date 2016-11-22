from unittest import TestCase
from unittest.mock import patch, MagicMock

from db import PrzystankiDb


class PrzystankiDbTests(TestCase):
    def setUp(self):
        super().setUp()
        self.environ_dict = {
            'TRAM_ROOT': 'mock_value'
        }
        self.os_environ_mock = patch.dict('db.przystanki.os.environ', self.environ_dict).start()
        self.sqlite_mock = patch('db.przystanki.sqlite3').start()
        self.mock_db_connection = MagicMock()
        self.mock_db_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_db_cursor
        self.sqlite_mock.connect.return_value = self.mock_db_connection
        self.przystanki = PrzystankiDb()

    def tearDown(self):
        super().tearDown()

    def test_constructor_default(self):
        mock_db_file = self.environ_dict['TRAM_ROOT'] + '/data/przystanki.db'
        self.assertEqual(self.przystanki.db_file, mock_db_file)
        self.sqlite_mock.connect.assert_called_once_with(mock_db_file)
        self.mock_db_connection.cursor.assert_called_once_with()
        self.assertEqual(self.przystanki.cursor, self.mock_db_cursor)

    def test_clear_table(self):
        self.przystanki.clear_table()
        self.mock_db_cursor.execute.assert_called_once_with('delete from przystanki')
        self.mock_db_connection.commit.assert_called_once_with()

    def test_insert_success(self):
        stuff_dict = {
            'pointId': 'mock_point_id',
            'variantId': 'mock_variant_id',
            'lineName': 'mock_line_name',
            'pointTime': 'mock_point_time',
            'pointName': 'mock_point_name',
            'route': 'mock_route'
        }
        self.przystanki.insert(stuff_dict)
        self.assertTrue(self.mock_db_cursor.execute.called)
        self.assertEqual(self.mock_db_cursor.execute.call_count, 1)
        self.assertTrue(self.mock_db_connection.commit.called)

    def test_insert_missing_keys(self):
        stuff_dict = {
            'pointId': 'mock_point_id',
        }
        with self.assertRaises(KeyError):
            self.przystanki.insert(stuff_dict)
        self.assertFalse(self.mock_db_cursor.execute.called)
        self.assertEqual(self.mock_db_cursor.execute.call_count, 0)
        self.assertFalse(self.mock_db_connection.commit.called)

    def test_get_point_time(self):
        return_dict = {
            'pointName': 'mock_point_name',
            'pointTime': {'point': 'time'},
            'route': 'mock_point_route'
        }
        self.mock_db_cursor.fetchall.return_value = [(return_dict['pointName'], '{"point": "time"}', return_dict['route'])]
        ret = self.przystanki.get_point_time(None, None, None)
        self.assertEqual(ret, return_dict)
        self.assertTrue(self.mock_db_cursor.execute.called)
        self.assertEqual(self.mock_db_cursor.execute.call_count, 1)
        self.mock_db_cursor.fetchall.assert_called_once_with()
