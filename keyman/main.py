import sys

from fabric.api import env
from fabric.colors import green, blue, yellow
from fabric.context_managers import quiet
from fabric.decorators import task
from fabric.operations import prompt
from fabric.main import main

from helpers import KeysFile


def keymanager_main():
    """
    Override the interface to Fabric so we can list tasks off by default
    """
    if len(sys.argv) < 2:
        sys.argv.append('-l')
    main(fabfile_locations=[__file__.replace('pyc', 'py')])


@task
def list_users():
    """
    Read the contents of a servers authorized_keys file

        e.g: keymanager list_users --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()

    print(green('\n================== {}:'.format(env.host_string)))
    for user in keyfile.users:
        print(blue('\t ' + user.name))


@task
def add_user(key_or_path=None):
    """
    Add a user to a server using the given identity file

        e.g keymanager add_user --hosts user@host
            keymanager add_user:~/.ssh/id_rsa.pub --hosts user@host
            keymanager add_user:ssh-rsa KEY_HASH user@host --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()
        if key_or_path is None:
            user = prompt(green("Paste key or file path:") + "\n\n",
                          validate=keyfile.validate_user)
        else:
            user = keyfile.validate_user(key_or_path)

    if keyfile.add_user(user):
        print(green('{} authorized'.format(user.name, env.host_string)))
    else:
        print(yellow('{} already authorized, skipping'.format(user.name)))


@task
def delete_user(username=None):
    """
    Remove a user from a server

        e.g keymanager delete_user --hosts user@host
            keymanager delete_user:user@host --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()

    if username is None:
        username = prompt(green("Username: "))

    removed = keyfile.delete_user(username)

    if removed:
        print(green('{} removed'.format(username, env.host_string)))
    else:
        print(yellow('{} not in keys, skipping'.format(username)))
