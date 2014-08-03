keymanager
==========

SSH Key manager, powered by fabric

When controlling access to various servers for various people, it can become
quite difficult/tedious to manage, for some people its acceptable to pass
around one common keyfile, but this presents the problem that if any user ever
leaves, the keyfile will need replacing, and re-distributing to all users.

A way to get around this problem, and be generally more secure, is to use
individual public keys, if a user needs access to one or more servers, they
give you their public key, and you put it into the `authorized_keys` file on
the user account/server they need access to.

Doing this manually, e.g:

    ssh user@host
    echo "ssh-rsa KEY_HASH user@host" >> ~/.authorized_keys

Can become tedious to manage, so I wrote a manager that allows you to manage
keys on multiple servers very easily, it uses the already amazing [fabric](https://github.com/fabric/fabric)
library.

### Setup (production)

    pip install git+git://github.com/farridav/keymanager.git

\* Will be on pypi soon, see [Issue 2](https://github.com/farridav/keymanager/issues/2)

### Setup (development)

#### Clone the project

    git clone git@github.com:farridav/keymanager.git
    cd keymanager

#### Install requirements

    pip install -r test-requirements.txt

#### Run the tests

    nosetests

### Using it

#### List available commands

    keymanager

#### Get more details/examples for a command (same as fabric)

    keymanager -d <task_name>

#### List users

    keymanager list_users --hosts user@host,otheruser@otherhost

#### Add a new user

##### User prompt

    keymanager add_user --hosts user@host

##### By path to key

    keymanager add_user:~/.ssh/id_rsa.pub --hosts user@host

##### By direct key

    keymanager add_user:ssh-rsa KEY_HASH user@host --hosts user@host

#### Delete a user

##### User prompt

    keymanager delete_user --hosts user@host

##### By Username

    keymanager delete_user:user@host --hosts user@host
