from collections import namedtuple
from datetime import datetime
from fabric.api import run, env
from fabric.decorators import task, hosts
from fabric.context_managers import quiet
from fabric.colors import green, blue, yellow


class KeysFile(object):

    def __init__(self, key_file='~/.ssh/test_authorized_keys'):
        self.keys = run('cat {}'.format(key_file)).split('\n')
        self.users = [self.get_user(key) for key in self.keys]
        self.hashes = [user.hash for user in self.users]

    def get_user(self, key):
        user = namedtuple('User', ['keytype', 'hash', 'name'])
        key_parts = key.split()
        user.keytype = key_parts[0]
        user.hash = key_parts[1]
        user.name = 'anonymous'

        # If we have a name
        if len(key_parts) == 3:
            user.name = key_parts[2]

        return user

    def purge_users(self):
        """
        Clean authorized_keys except for the given users
        """
        allowed_users = [
            'info@test.co.uk', 'info@other.co.uk',
            'info@davidfarrington.co.uk'
        ]

        run(
            'sed \'/\({hosts}\)/ ! D\' -i-{timestamp}.old {key_file}'.format(
                hosts='\|'.join(allowed_users),
                timestamp=datetime.now().strftime('%s'),
                key_file=self.key_file
            )
        )

    def add_user(self, identity_file):
        """
        Add a user to a server using the given identity file
        """
        with quiet():
            key = run('cat {}'.format(identity_file))
            new_user = self.get_user(key)
            added = False

            if new_user.hash not in self.hashes:
                run('echo "{}" >> ~/.ssh/test_authorized_keys'.format(key))
                added = True

            return new_user, added

    def remove_user(self, user):
        """
        Remove a user from a server
        """
        with quiet():
            run("sed '/{}/ ! D' -i_egg.old ~/.ssh/test_authorized_keys".format(user))

            key = run('cat {}'.format(identity_file))
            new_user = self.get_user(key)
            added = False

            if new_user.hash not in self.hashes:
                run('echo "{}" >> ~/.ssh/test_authorized_keys'.format(key))
                added = True

            return new_user, added


@task
@hosts('david@127.0.0.1')
def list_users():
    """
    Read the contents of a servers authorized_keys file
    """
    with quiet():
        keyfile = KeysFile()

    print(green('\n================== {}:'.format(env.host_string)))
    for user in keyfile.users:
        print(blue('\t ' + user.name))


@task
@hosts('david@127.0.0.1')
def add_user(key='~/.ssh/keys/id_rsa.pub'):
    """
    Add a user to a server using the given identity file
    """
    with quiet():
        keyfile = KeysFile()

    user, added = keyfile.add_user(key)

    if added:
        print(green('{} authorized'.format(user.name, env.host_string)))
    else:
        print(yellow('{} already authorized, skipping'.format(user.name)))


@task
@hosts('david@127.0.0.1')
def delete_user(user='info@davidfarrington.co.uk'):
    """
    Remove a user from a server
    """
    with quiet():
        keyfile = KeysFile()

    user, removed = keyfile.remove_user(user)

    if removed:
        print(green('{} removed'.format(user, env.host_string)))
    else:
        print(yellow('{} not in keys, skipping'.format(user)))
