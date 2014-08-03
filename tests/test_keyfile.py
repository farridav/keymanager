from unittest import TestCase
from mock import Mock, patch

from keyman.helpers import KeysFile


class TestKeyFile(TestCase):

    @classmethod
    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.run')
    def setupClass(cls, run_command):
        run_command.return_value = open('tests/authorized_keys', 'r').read()
        cls.keyfile = KeysFile()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_user_list(self):
        self.assertTrue(len(self.keyfile.users) > 0)
        pass

    def test_add_user(self):
        pass

    def test_delete_user(self):
        pass
