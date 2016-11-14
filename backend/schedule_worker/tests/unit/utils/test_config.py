from unittest import main, TestCase
from unittest.mock import patch, mock_open

from utils import Config


class TestConfig(TestCase):

    def setUp(self):
        super().setUp()
        self.environ_dict = {
            'TRAM_ROOT': 'mock_value'
        }
        self.config_dict = {
            'mock_key': 'mock_value'
        }
        self.josn_load_mock = patch('utils.config.json.load', return_value=self.config_dict).start()
        self.os_environ_mock = patch.dict('utils.config.os.environ', self.environ_dict).start()
        self.m = mock_open()
        with patch('utils.config.open', self.m, create=True):
            self.config = Config()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

        Config._instance = None

    def test_constructor_path_provided(self):
        Config._instance = None
        mock_path = '/mock/path/to/config'
        m = mock_open()
        with patch('utils.config.open', m, create=True):
            config = Config(mock_path)

        m.assert_called_once_with(mock_path, 'r')
        self.assertEqual(config.cfg, self.config_dict)
        self.assertEqual(config.path, mock_path)
        self.assertTrue(self.josn_load_mock.called)

    def test_constructor_default_path(self):
        self.m.assert_called_once_with('mock_value/conf/config.json', 'r')
        self.assertEqual(self.config.cfg, self.config_dict)
        self.assertEqual(self.config.path, 'mock_value/conf/config.json')
        self.assertTrue(self.josn_load_mock.called)

    def test_get_item_no_default(self):
        ret = self.config.get('mock_key')
        self.assertEqual(self.config_dict['mock_key'], ret)

    def test_get_item_with_default_key_exist(self):
        ret = self.config.get('mock_key', default='another mock value')
        self.assertEqual(self.config_dict['mock_key'], ret)

    def test_get_item_with_default_key_dont_exist(self):
        ret = self.config.get('not_mock_key', default='another mock value')
        self.assertEqual('another mock value', ret)

    def test_set(self):
        ret = self.config.set('another_mock_key', 'another_mock_value')
        self.assertIsNone(ret)
        self.assertTrue('another_mock_key' in self.config.cfg)
        self.assertEqual(self.config.cfg['another_mock_key'], 'another_mock_value')

    def test_dump(self):
        mock_json_dump = patch('utils.config.json.dump').start()
        m = mock_open()
        with patch('utils.config.open', m, create=True):
            self.config.dump()

        self.assertTrue(mock_json_dump.called)
        mock_json_dump.assert_called_once_with(self.config_dict, m(), indent=4)



    def test__getitem__(self):
        ret = self.config['mock_key']
        self.assertEqual(ret, 'mock_value')

    def test_contains_true(self):
        ret = 'mock_key' in self.config
        self.assertTrue(ret)

    def test_contains_false(self):
        ret = 'not_mock_key' in self.config
        self.assertFalse(ret)
