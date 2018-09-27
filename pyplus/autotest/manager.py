
import os
import asyncio

from pyplus import singleton
from pyplus.autotest.node import Node
from pyplus.importer import import_python

@singleton
class Manager(object):
    def __init__(self, name='AutoTest'):
        self.__root = Node(name)
        self.__current = self.__root
        self.__stack = []


    def __call__(self, *args, **kwargs):
        self.__root()
        asyncio.get_event_loop().close()

    def add(self, *args, **kwargs):
        self.__current = self.__current.add(*args, **kwargs)
        return self.__current

    def __push(self): self.__stack.append(self.__current)

    def __pop(self): self.__current = self.__stack.pop(0)

    def scan(self, path, exclude=[]):

        def _scan(path):
            files = os.listdir(path)
            for f in files:
                name = os.path.basename(f)
                if os.path.isdir(f):
                    self.__push()
                    self.add(name)
                    _scan(f)
                    self.__pop()
                else:
                    if os.path.splitext(name)[-1] != '.py' or \
                        name in exclude:
                        continue
                    self.__push()
                    self.add(name)
                    import_python(f)
                    self.__pop()

        _scan(path)
        self.__root.remove_unused()



