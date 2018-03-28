from .layout import Line


class PyImport(Line):
    def __init__(self, name, k_from=None, k_as=None):
        super(PyImport, self).__init__(None)
        self.name = name
        self.k_from = k_from
        self.k_as = k_as

    def __compile__(self):
        code = ''
        if self.k_from is not None: code += 'from {} '.format(self.k_from)
        code += 'import {} '.format(self.name)
        if self.k_as is not None: code += 'as {}'.format(self.k_as)

        self._code = code
        return super(PyImport, self).__compile__()


def pyimport(name, k_from=None, k_as=None): return PyImport(name, k_from, k_as)

def from_import(name, k_from=None): return PyImport(name, k_from)

def from_import_as(name, k_from=None, k_as=None): return PyImport(name, k_from, k_as)

def import_as(name, k_as): return PyImport(name, k_as=k_as)


