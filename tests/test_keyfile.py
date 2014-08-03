from unittest import TestCase
from mock import Mock, patch

from keyman.helpers import KeysFile

from factories import UserFactory


class TestKeyFile(TestCase):

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys')
    def test_user_list(self, read_keys):
        """
        When we load in a keyfile wit 3 users, they are available for listing
        """
        read_keys.return_value = \
            [user.full_key for user in UserFactory.stub_batch(3)]
        keyfile = KeysFile()

        self.assertEqual(len(keyfile.users), 3)

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys')
    @patch('keyman.helpers.run')
    def test_add_user(self, run_command, read_keys):
        """
        When we try to add a user, the correct command is given
        """
        read_keys.return_value = [UserFactory().full_key]
        user = UserFactory()
        keyfile = KeysFile()
        keyfile.add_user(user)

        run_command.assert_called_with(
            'echo "{key_type} {key_hash} {username}" >> {key_file}'.format(
                key_type=user.keytype,
                key_hash=user.hash,
                username=user.name,
                key_file=keyfile.key_file
            )
        )

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys')
    @patch('keyman.helpers.run')
    def test_delete_user(self, run_command, read_keys):
        """
        When we delete a user, the correct command is used
        """
        user = UserFactory()
        read_keys.return_value = [user.full_key]
        keyfile = KeysFile()
        result = keyfile.delete_user(user.name)

        self.assertTrue(result)
        run_command.assert_called_with('sed -i \'/{}/d\' {}'.format(
            user.name, keyfile.key_file))
