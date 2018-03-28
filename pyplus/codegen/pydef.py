from .layout import Block, Line



class PyDef(Block):
    def __init__(self, name, args, contents):
        super(PyDef, self).__init__(None, None)
        self.__name = name
        self.__args = args or []
        self.__contents = contents
        self.__decorator = None

    def __compile__(self):
        self._headers = []

        # decorator
        if self.__decorator is not None:
            if not isinstance(self.__decorator, (str, Line)):
                raise Exception('invalid decorator type: {}, type must be str or Line'.format(type(self.__decorator)))
            self._headers.append(self.__decorator)

        # method
        method = ''
        method += 'def {}('.format(self.__name)
        for i in range(len(self.__args)):
            method += self.__args[i]
            if i < len(self.__args)-1: method += ', '
        method += '): '
        self._headers.append(method)

        # contents
        self._layouts = self.__contents

        return super(PyDef, self).__compile__()


    def decorator(self, s): self.__decorator = s; return self



def pydef(name, *args):
    if len(args) == 0: raise Exception('must be define contents of def')
    if len(args) == 1: return PyDef(name, None, args[0])
    else: return PyDef(name, args[0], args[1])

def member(name, *args):
    if len(args) == 0: raise Exception('must be define contents of def')
    if len(args) == 1: return PyDef(name, ['self'], args[0])
    else: return PyDef(name, ['self']+args[0], args[1])

def static(name, *args): return pydef(name, *args).decorator('@staticmethod')

def getter(name, contents): return member(name, contents).decorator('@property')

def setter(name, *args):
    decorator = '@{}.setter'.format(name)
    if len(args) == 0: raise Exception('must be define contents of def')
    if len(args) == 1: return member(name, ['v'], args[0]).decorator(decorator)
    else: return member(name, args[0], args[1]).decorator(decorator)