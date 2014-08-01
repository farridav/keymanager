from collections import namedtuple
from fabric.api import run, env, abort
from fabric.decorators import task
from fabric.context_managers import quiet
from fabric.colors import green, blue, yellow
from fabric.contrib.files import exists
from fabric.operations import prompt


class KeysFile(object):

    def __init__(self, key_file='~/.ssh/test_authorized_keys'):
        if not exists(key_file):
            abort('SSH key file not found')

        self.key_file = key_file
        self.keys = [
            key for key in run('cat {}'.format(key_file)).split('\n') if key
        ]
        self.users = [self.get_user(key) for key in self.keys]
        self.hashes = [user.hash for user in self.users]

    def get_user(self, key):
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
        Add a user to a server using the given identity file
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
        Remove a user from a server
        """
        with quiet():
            user = [user for user in self.users if user.name == username]
            if user:
                run('sed -i \'/{}/d\' {}'.format(user, self.key_file))
                return True
            return False


@task
def list_users():
    """
    Read the contents of a servers test_authorized_keys file

        e.g: fab list_users --hosts david@127.0.0.1

    """
    with quiet():
        keyfile = KeysFile()

    print(green('\n================== {}:'.format(env.host_string)))
    for user in keyfile.users:
        print(blue('\t ' + user.name))


@task
def add_user():
    """
    Add a user to a server using the given identity file

        e.g fab add_user --hosts david@127.0.0.1

    """
    with quiet():
        keyfile = KeysFile()
        user = prompt(green("Paste key or file path:") + "\n\n",
                      validate=keyfile.validate_user)

    if keyfile.add_user(user):
        print(green('{} authorized'.format(user.name, env.host_string)))
    else:
        print(yellow('{} already authorized, skipping'.format(user.name)))


@task
def delete_user(username=None):
    """
    Remove a user from a server

        e.g fab delete_user --hosts david@127.0.0.1

    """
    with quiet():
        keyfile = KeysFile()

    if not username:
        username = prompt(green("Username: "))

    removed = keyfile.delete_user(username)

    if removed:
        print(green('{} removed'.format(username, env.host_string)))
    else:
        print(yellow('{} not in keys, skipping'.format(username)))
