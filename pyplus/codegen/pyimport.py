from pyplus.codegen.layout import Line


class PyImport(Line):
    def __reset__(self, name, k_from=None, k_as=None):
        self.__name = name
        self.__from = k_from
        self.__as = k_as

        text = ''
        if self.__from is not None: text += 'from {} '.format(self.__from)
        text += 'import {} '.format(self.__name)
        if self.__as is not None: text += 'as {}'.format(self.__as)

        return super(PyImport, self).__reset__(text)



def pyimport(name, k_from=None, k_as=None): return PyImport(name, k_from, k_as)

def from_import(k_from, name): return PyImport(name, k_from)

def from_import_as(k_from, name, k_as): return PyImport(name, k_from, k_as)

def import_as(name, k_as): return PyImport(name, k_as=k_as)


