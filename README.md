keymanager
==========

SSH Key manager, powered by fabric

I control access to servers that a team of people need access to, and i dont want to use a generic private key file,
as I will need to change it and redistribute every time a team member leaves, so i use public keys.

It got very tedious doing this manually, something like:

    ssh username@1.2.3.4 echo "ssh-rsa KEY-HASH-HERE user@domain.com" >> ~/.ssh/authorized_keys

I could of used my ssh agent, and made use of `ssh-copy-id` but thats also highly impractical, so I wrote a fabric
powered key manager that allows me to add, remove and list ssh keys for any number of hosts at a time.


### Set it up

    git clone git@github.com:farridav/keymanager.git
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt

### Use it

#### List users

    fab list_users --hosts user@host,otheruser@otherhost

#### Add a new user

    fab add_user --hosts user@host

#### Delete a user

    fab delete_user --hosts user@host
