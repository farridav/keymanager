import os
import sys

from fabric.api import env, abort
from fabric.colors import green, blue, yellow, red
from fabric.context_managers import quiet
from fabric.decorators import task
from fabric.contrib.console import confirm, prompt
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
def list():
    """
    Read the contents of a servers authorized_keys file

        e.g: keymanager lists --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()

    print(green('\n================== {}:'.format(env.host_string)))
    for user in keyfile.users:
        print(blue('\t ' + user.name))


@task
def add(key_or_path=None):
    """
    Add a user to a server using the given identity file

        e.g keymanager add --hosts user@host
            keymanager add:~/.ssh/id_rsa.pub --hosts user@host
            keymanager add:ssh-rsa KEY_HASH user@host --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()
        if key_or_path is None:
            user = prompt(green("Enter key or file path:") + "\n\n",
                          validate=keyfile.get_user)
        else:
            user = keyfile.get_user(key_or_path)

    if keyfile.add(user):
        print(green('{} authorized'.format(user.name)))
    else:
        print(yellow('{} already authorized, skipping'.format(user.name)))


@task
def add_batch(key_file, replace=False, force=False):
    """
    Add a batch of users to a server using the given file, set replace to True
    if you wish to remove any users not in given key_file. The `force`
    argument has been added so this task can be called with no user input

        e.g keymanager add_batch:~/key_file.txt --hosts user@host
            keymanager add_batch:~/key_file.txt,replace=True --hosts user@host
            keymanager add_batch:~/key_file.txt,replace=True,force=True \
                --hosts user@host

    """
    if not os.path.isfile(key_file):
        abort('File {} does not exist'.format(key_file))

    with quiet():
        keyfile = KeysFile()
        new_users = [keyfile.get_user(user) for user in
                     keyfile.read_keys(key_file)]

        # Users that are not in our file
        user_diff = [user for user in keyfile.users if user.hash not
                     in [new_user.hash for new_user in new_users]]

        # If we want to remove unspecified users
        if user_diff and replace:
            usernames = '\n\t'.join([user.name for user in user_diff])
            if force:
                remove = True
            else:
                remove = confirm(
                    red('Remove users ?:\n\t{}'.format(usernames)),
                    default=False
                )

            if remove:
                for user in user_diff:
                    if keyfile.delete_user(user.name):
                        print(green('{} removed'.format(user.name)))

        # now add the new users
        for user in new_users:
            if keyfile.add_user(user):
                print(green('{} authorized'.format(user.name)))
            else:
                print(yellow('{} already authorized'.format(user.name)))


@task
def delete(username=None):
    """
    Remove a user from a server

        e.g keymanager delete --hosts user@host
            keymanager delete:user@host --hosts user@host

    """
    with quiet():
        keyfile = KeysFile()

    if username is None:
        username = prompt(green("Username: "))

    if keyfile.delete(username):
        print(green('{} removed'.format(username)))
    else:
        print(yellow('{} not in keys, skipping'.format(username)))


@task
def delete_batch(key_file, force=False):
    """
    Delete a batch of users to a server using the given file, the `force`
    argument has been added so this task can be called with no user input

        e.g keymanager delete_batch:~/key_file.txt --hosts user@host
            keymanager delete_batch:~/key_file.txt,force=True --hosts user@host

    """
    if not os.path.isfile(key_file):
        abort('File {} does not exist')

    with quiet():
        keyfile = KeysFile()
        users = [keyfile.get_user(user) for user in
                 keyfile.read_keys(key_file)]
        usernames = '\n\t'.join([user.name for user in users])

        if force:
            remove = True
        else:
            remove = confirm(
                red('Remove users ?:\n\t{}'.format(usernames)), default=False)

        if remove:
            for user in users:
                if keyfile.delete(user.name):
                    print(green('{} removed'.format(user.name)))
                else:
                    print(yellow('{} not in keys, skipping'.format(user.name)))
