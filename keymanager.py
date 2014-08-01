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
    If we call keymanager with no arguments, pass in fabrics `-l` arg to list
    of available tasks, then call fabrics own `main` function
    """
    if len(sys.argv) == 1:
        sys.argv.append('-l')
    return main(fabfile_locations=['keymanager.py'])


@task
def list_users():
    """
    Read the contents of a servers authorized_keys file

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
