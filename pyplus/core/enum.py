from __future__ import absolute_import, division, print_function

class Enum(object):
    __a = 1
    def __init__(self, **enums):
        #print(enums)
        object.__setattr__(self, "__edict", {})
        edict = object.__getattribute__(self, "__edict")
        for (k, v) in enums.items():
            edict[k] = v

    def __getattr__(self, key):
        edict = object.__getattribute__(self, "__edict")
        return edict.get(key, None)

    def __setattr__(self, key, value): assert False  # can not set attribute for enum

    def __str__(self):
        return "{0} {1}".format(object.__str__(self), object.__getattribute__(self, "__edict"))

    @property
    def keys(self): return object.__getattribute__(self, "__edict").keys()

    @property
    def values(self): return  object.__getattribute__(self, "__edict").values()

    def get_key(self, value):
        edict = object.__getattribute__(self, "__edict")
        ret = []
        for (k, v) in edict.items():
            if v == value:
                ret.append(k)
        return len(ret) == 0 and None or len(ret) == 1 and ret[0] or ret


enum = Enum
