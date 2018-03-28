from .layout import Block, Line



class PyClass(Block):
    def __init__(self, name, parent, contents):
        super(PyClass, self).__init__(None, None)
        self.__name = name
        self.__parent = parent or ''
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
        cls = 'class {}({}):'.format(self.__name, self.__parent)
        self._headers.append(cls)

        # contents
        self._layouts = self.__contents

        return super(PyClass, self).__compile__()


    def decorator(self, s):  self.__decorator = s



def pyclass(name, *args):
    if len(args) == 0: raise Exception('must be define contents of class')
    if len(args) == 1: return PyClass(name, None, args[0])
    else: return PyClass(name, args[0], args[1])