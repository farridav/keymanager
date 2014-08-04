from unittest import TestCase
from mock import Mock, patch

from keyman.helpers import KeysFile

from factories import UserFactory


class TestKeyFile(TestCase):
    """
    Test the keyfile class,

    There is a lot of patching going on here, perhaps more than is needed.
    TODO: make the tests clearer and patch more concisely
    """

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys')
    def test_user_list(self, read_keys):
        """
        When we load in a keyfile with 3 users, they are available for listing
        """
        users = UserFactory.stub_batch(3)
        read_keys.return_value = [user.full_key for user in users]
        keyfile = KeysFile()

        self.assertEqual(len(keyfile.users), 3)
        self.assertListEqual(
            [user.hash for user in keyfile.users],
            [user.hash for user in users]
        )

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

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys', Mock(return_value=[]))
    def test_get_user_anonymous(self):
        """
        We can have users that don't use identifiers
        """
        keyfile = KeysFile()
        user = keyfile.get_user(UserFactory(name='').full_key)

        self.assertEqual(user.name, 'anonymous')

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys', Mock(return_value=[]))
    @patch('keyman.helpers.os.path.isfile', Mock(return_value=True))
    @patch('keyman.helpers.local')
    def test_get_user_with_path(self, local_command):
        """
        We can get a user using a path to a key, as well as a key
        """
        user = UserFactory()
        local_command.return_value = user.full_key
        keyfile = KeysFile()
        fetched_user = keyfile.get_user('/path/to/key.pub')

        self.assertEqual(fetched_user.hash, user.hash)

    @patch('keyman.helpers.exists', Mock(return_value=True))
    @patch('keyman.helpers.KeysFile.read_keys', Mock(return_value=[]))
    @patch('sys.stderr', Mock())
    def test_malformed_key(self):
        """
        If we try to create a user with a malformed key, we abort
        """
        malformed_key = 'badly formed key in here'
        keyfile = KeysFile()

        with self.assertRaises(SystemExit):
            keyfile.get_user(malformed_key)
