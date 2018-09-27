import types

class Node(object):
    def __init__(self, name, desc=None, exec=None):
        self.__name = name
        self.__desc = desc
        self.__exec = exec
        self.__childs = []
        self.__parent = Node


    def __str__(self): return self.__name

    def __repr__(self): return self.__str__()


    def __call__(self, level=0):
        if len(self.__childs) == 0:
            if self.__exec is None: return
            self.__print(level, 'test {} ... '.format(self.__name), end='')
            result = self.__execute()
            print('ok' if result else 'fail')

        else:
            self.__print(level, self.__name)
            for c in self.__childs: c(level+1)

    @property
    def parent(self): return self.__parent

    @parent.setter
    def parent(self, p): self.__parent = p

    @property
    def avaliable(self):
        if len(self.__childs) == 0: return self.__exec is not None
        for c in self.__childs:
            if c.avaliable: return True
        return False


    def add(self, *args, **kwargs):
        node = Node(*args, **kwargs)
        self.__childs.append(node)
        node.parent = self
        return node


    def remove_unused(self):
        for i in range(len(self.__childs)-1, -1, -1):
            c = self.__childs[i]
            if c.avaliable:
                c.remove_unused()
            else:
                del self.__childs[i]


    def __print(self, level, c, end='\n'):
        content = ''
        content += ' ' * (level * 2)
        content += '' if level == 0 else '|-- '
        content += c
        print(content, end=end)



    def __execute(self):
        if self.__exec is None: return
        if type(self.__exec) is types.CoroutineType:
            import asyncio
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.__exec)
        else:
            return self.__exec()


