from pyplus.codegen.layout import Line


class PyImport(Line):
    def __init__(self, *args, **kwargs): super(PyImport, self).__init__(*args, **kwargs)

    def _reset(self, name, _from=None, _as=None):
        self.__name = name
        self.__from = _from
        self.__as = _as

        text = ''
        if self.__from is not None: text += 'from {} '.format(self.__from)
        text += 'import {} '.format(self.__name)
        if self.__as is not None: text += 'as {}'.format(self.__as)

        return super(PyImport, self)._reset(text)



def pyimport(name, _from=None, _as=None): return PyImport(name, _from, _as)

def from_import(_from, name): return PyImport(name, _from)

def from_import_as(_from, name, _as): return PyImport(name, _from, _as)

def import_as(name, _as): return PyImport(name, _as=_as)


