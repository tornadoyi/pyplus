from pyplus.codegen.layout import Block

class Decorator(Block):
    def _reset(self, decorators, statement, contents):
        self.__decorators = decorators
        self.__statement = statement
        self.__contents = contents

        decorators = decorators if isinstance(decorators, (tuple, list)) else [decorators]
        super(Decorator, self)._reset(decorators+[statement], contents)


    def decorator(self, ds):
        ds = ds if isinstance(ds, (tuple, list)) else [ds]
        super(Decorator, self)._reset(self.__decorators+ds+[self.__statement], self.__contents)
        return self


    def staticmethod(self): return self.decorator('@staticmethod')

    def property(self): return self.decorator('@property')

    def setter(self, name): return self.decorator('@{}.setter'.format(name))