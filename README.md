keymanager
==========

SSH Key manager, powered by fabric

I control access to servers that a team of people need access to, and i dont want to use a generic private key file,
as I will need to change it and redistribute every time a team member leaves, so i use public keys.

It got very tedious doing this manually, something like:

    ssh username@1.2.3.4 echo "ssh-rsa KEY-HASH-HERE user@domain.com" >> ~/.ssh/authorized_keys

I could of used my ssh agent, and made use of `ssh-copy-id` but thats also highly impractical, so I wrote a fabric
powered key manager that allows me to add, remove and list ssh keys for any number of hosts at a time.


### Set it up (production)

    pip install git+git://github.com/farridav/keymanager.git

\* Will be on pypi soon, see [Issue 2](https://github.com/farridav/keymanager/issues/2)

### Set it up (development)

    git clone git@github.com:farridav/keymanager.git
    cd keymanager
    pip install -r requirements.txt

### Use it

#### List available commands

    keymanager

#### List users

    keymanager list_users --hosts user@host,otheruser@otherhost

#### Add a new user

    keymanager add_user --hosts user@host

#### Delete a user

    keymanager delete_user --hosts user@host
