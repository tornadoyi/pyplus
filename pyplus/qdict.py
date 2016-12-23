import copy

class qdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self.merge(*args, **kwargs)

    def __getattr__(self, item):
        return dict.get(self, item, None)

    def __setattr__(self, key, value):
        dict.__setitem__(self, key, value)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        d = copy.deepcopy(dict(self))
        return type(self)(**d)

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        for (k, v) in state.items():
            self.__setitem__(k, v)


    def merge(self, *args, **kwargs):
        for arg in args:
            d = None
            if type(arg) == dict:
                d = arg
            elif hasattr(arg, '__dict__'):
                d = arg.__dict__
            else:
                continue
            for (k, v) in d.items():
                self.__setitem__(k, v)

        for (k, v) in kwargs.items():
            self.__setitem__(k, v)


if __name__ == '__main__':
    d = qdict(a=1, b=2, c=3)

    # test pickle
    import pickle
    en = pickle.dumps(d)
    de = pickle.loads(en)
    print(de == d)

    # test inherit
    class Test(qdict):
        pass
    t = Test(x=1, y=2)
    ct = copy.deepcopy(t)
    print(type(ct) == type(t))

    