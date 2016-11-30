
class qdict(dict):
    def __getattr__(self, item):
        return dict.get(self, item, None)

    def __setitem__(self, key, value):
        self.setdefault(key, value)
