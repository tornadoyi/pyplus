from pyplus.codegen.decorator import Decorator



class PyClass(Decorator):
    def __reset__(self, name, parent, contents):
        self.__name = name
        self.__parent = parent or ''
        self.__contents = contents

        # method
        cls = 'class {}({}):'.format(self.__name, self.__parent)

        super(PyClass, self).__reset__([], cls, self.__contents)



def pyclass(name, *args):
    if len(args) == 0: raise Exception('must be define contents of class')
    if len(args) == 1: return PyClass(name, None, args[0])
    else: return PyClass(name, args[0], args[1])