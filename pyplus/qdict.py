import copy

class qdict(dict):
    def __init__(self, *args, **kwargs):
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

    def __getattr__(self, item):
        return dict.get(self, item, None)

    def __setattr__(self, key, value):
        dict.__setitem__(self, key, value)

    def __deepcopy__(self, memo):
        return qdict(copy.deepcopy(dict(self)))


