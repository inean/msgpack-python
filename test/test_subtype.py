#!/usr/bin/env python
# coding: utf-8

from msgpack import packb, unpackb, Packer, ExtType, Unpacker
from collections import namedtuple

class MyList(list):
    pass

class MyDict(dict):
    pass

class MyTuple(tuple):
    pass

MyNamedTuple = namedtuple('MyNamedTuple', 'x y')

def test_types():
    assert packb(MyDict()) == packb(dict())
    assert packb(MyList()) == packb(list())

def test_namedtuple():
    def default(obj):
        print('default called', obj)
        if hasattr(obj, '_asdict'):
            typecode = 123 # application specific typecode
            data = packb([obj.__class__.__name__, obj._asdict().items()])
            return ExtType(typecode, data)
        raise TypeError("Unknwon type object %r" % (obj,))

    def ext_hook(code, data):
        assert code == 123
        obj = unpackb(data)
        cls = namedtuple(obj[0], " ".join([x[0] for x in obj[1]]))
        print obj[0], " ".join([x[0] for x in obj[1]])
        return cls(*[x[1] for x in obj[1]])
    pack = packb(MyNamedTuple(1, 2), default=default)
    upack = unpackb(pack, ext_hook=ext_hook)
    assert MyNamedTuple(1, 2) == upack
