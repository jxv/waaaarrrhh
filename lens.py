import copy
import functools

class Lens:
    def __init__(self, getter, putter):
        self.getter = getter
        self.putter = putter

    def __rshift__(self, second):
        def getter(o):
            return second.getter(self.getter(o))
        def putter(o, v):
            return self.putter(o, second.putter(self.getter(o), v))
        return Lens(getter, putter)

    def __lshift__(self, second):
        return second >> self

def get(l, o):
    return l.getter(o)

def put(l, o, v):
    return l.putter(o, v)

def over(l, o, f):
    return l.putter(o, f(l.getter(o)))

def key(k):
    def getter(o):
        return o[k]
    def putter(o, v):
        r = copy.copy(o)
        r[k] = v
        return r
    return Lens(getter, putter)

def keys(ks):
    l = functools.reduce(lambda a, b: a >> b, map(key, ks), Lens(lambda o: o, lambda _, v: v))
    def getter(o):
        return get(l, o)
    def putter(o, v):
        return put(l, o, v)
    return Lens(getter, putter)
