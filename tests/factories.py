import factory


class UserFactory(factory.StubFactory):
    keytype = 'ssh-rsa'
    hash = factory.Sequence(lambda num: 'HASH{num}'.format(num=num))
    name = factory.Sequence(lambda num: 'user{num}@host{num}'.format(num=num))

    full_key = factory.LazyAttribute(
        lambda stub: '{} {} {}'.format(stub.keytype, stub.hash, stub.name))
