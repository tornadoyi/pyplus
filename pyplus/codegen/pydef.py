from pyplus.codegen.decorator import Decorator



class PyDef(Decorator):
    def _reset(self, name, args, contents):
        self.__name = name
        self.__args = args or []
        self.__contents = contents

        # method
        method = ''
        method += 'def {}('.format(self.__name)
        for i in range(len(self.__args)):
            method += self.__args[i]
            if i < len(self.__args) - 1: method += ', '
        method += '): '

        # merge contents and header to same line
        content, contents = '', []
        if len(self.__contents) == 1 and type(self.__contents[0]) == str:
            content = '{}'.format(self.__contents[0])
        else:
            contents = self.__contents

        super(PyDef, self)._reset([], method+content, contents)



def pydef(name, *args):
    if len(args) == 0: raise Exception('must be define contents for def')
    if len(args) == 1: return PyDef(name, None, args[0])
    else: return PyDef(name, args[0], args[1])

def member(name, *args):
    if len(args) == 0: raise Exception('must be define contents for def')
    if len(args) == 1: return PyDef(name, ['self'], args[0])
    else: return PyDef(name, ['self']+args[0], args[1])

def static(name, *args): return pydef(name, *args).staticmethod()

def getter(name, contents): return member(name, contents).property()

def setter(name, *args):
    if len(args) == 0: raise Exception('must be define contents of def')
    if len(args) == 1: return member(name, ['v'], args[0]).setter(name)
    else: return member(name, args[0], args[1]).setter(name)