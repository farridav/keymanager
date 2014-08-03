from collections import namedtuple

from fabric.api import run as run, abort
from fabric.context_managers import quiet
from fabric.contrib.files import exists


class KeysFile(object):
    """
    A helper class to represent an authorized_keys file
    """

    def __init__(self, key_file='~/.ssh/authorized_keys'):
        if not exists(key_file):
            abort('SSH key file not found')

        self.key_file = key_file
        self.keys = self.read_keys(self.key_file)
        self.users = [self.get_user(key) for key in self.keys]
        self.hashes = [user.hash for user in self.users]

    def read_keys(self, key_file):
        keys = run('cat {}'.format(key_file)).split('\n')
        return [key for key in keys if key]

    def get_user(self, key):
        """
        Given a public ssh key, return a user object

        If an invalid user is given, abort
        """
        user = namedtuple('User', ['keytype', 'hash', 'name', 'full_key'])
        user.full_key = key
        key_parts = key.split()

        if len(key_parts) < 2 or len(key_parts) > 3:
            abort('Malformed key: {}'.format(' '.join(key_parts)))

        user.keytype = key_parts[0]
        user.hash = key_parts[1]
        user.name = 'anonymous'

        # If we have a name
        if len(key_parts) == 3:
            user.name = key_parts[2]

        return user

    def add_user(self, user):
        """
        Add a user to a server using the given a valid user object
        """
        with quiet():
            added = False

            if user.hash not in self.hashes:
                run('echo "{}" >> {}'.format(user.full_key, self.key_file))
                added = True

            return added

    def validate_user(self, key):
        """
        If passed a key or a path, make a user out of it and return
        """
        if exists(key):
            key = run('cat {}'.format(key))
        return self.get_user(key)

    def delete_user(self, username):
        """
        Remove a user, given a username
        """
        with quiet():
            user = [user for user in self.users if user.name == username]
            if user:
                run('sed -i \'/{}/d\' {}'.format(user[0].name, self.key_file))
                return True
            return False
