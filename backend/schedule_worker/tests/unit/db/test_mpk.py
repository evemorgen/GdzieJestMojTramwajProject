from unittest import main, TestCase
from unittest.mock import patch, MagicMock

from db import MpkDb


class MpkDbTests(TestCase):
    def setUp(self):
        super().setUp()
        self.environ_dict = {
            'TRAM_ROOT': 'mock_value'
        }
        self.os_environ_mock = patch.dict('db.mpk.os.environ', self.environ_dict).start()
        self.sqlite_mock = patch('db.mpk.sqlite3').start()
        self.mock_db_connection = MagicMock()
        self.mock_db_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_db_cursor
        self.sqlite_mock.connect.return_value = self.mock_db_connection
        self.mpk = MpkDb()

    def tearDown(self):
        super().tearDown()

    def test_constructor_default(self):
        mock_db_file = self.environ_dict['TRAM_ROOT'] + '/data/baza.ready.zip'
        self.assertEqual(self.mpk.db_file, mock_db_file)
        self.sqlite_mock.connect.assert_called_once_with(mock_db_file)
        self.mock_db_connection.cursor.assert_called_once_with()
        self.assertEqual(self.mpk.cursor, self.mock_db_cursor)

    def test_get_lines(self):
        self.mock_db_cursor.fetchall.return_value = [(18,), (19,), (20,)]
        res = self.mpk.get_lines()
        self.assertEqual(res, [18, 19, 20])
        self.assertTrue(self.mock_db_cursor.execute.called)
        self.assertEqual(self.mock_db_cursor.execute.call_count, 1)

    def test_get_line_points(self):
        mock_line = 18
        mock_ret_dict = {963234: [11948, 9801, 9799], 963235: [7888, 9565]}
        self.mock_db_cursor.fetchall.return_value = [(963234, 11948), (963234, 9801), (963234, 9799), (963235, 7888), (963235, 9565)]
        ret = self.mpk.get_line_points(mock_line)
        self.assertEqual(ret, mock_ret_dict)
        self.assertTrue(self.mock_db_cursor.execute.called)
        self.assertEqual(self.mock_db_cursor.execute.call_count, 1)



