
from collections import OrderedDict

_OP_ADD = 0
_OP_DEL = 1


class Messager(object):
    def __init__(self):
        self.__listeners = OrderedDict()
        self.__listener_ops = []
        self.__lock = False


    def add_listener(self, listener, function=None):
        if self.__lock:
            self.__listener_ops.append((_OP_ADD, listener, function))
        else:
            self.__add_listener(listener, function)


    def del_listener(self, listener, function=None):
        if self.__lock:
            self.__listener_ops.append((_OP_DEL, listener, function))
        else:
            self.__del_listener(listener, function)


    def notify(self, function, *args, **kwargs): return self._on_notify(self, function , *args, **kwargs)


    def _on_notify(self, messager, function, *args, **kwargs):
        # notify
        self.__lock = True
        for l, functions in self.__listeners.items():
            if len(functions) > 0 and (function not in functions): continue
            f = getattr(l, function, None)
            if not f: continue
            f(*args, **kwargs, messager=messager)
        self.__lock = False

        # process delay ops
        self.__process_ops()



    def __add_listener(self, listener, function=None):
        functions = self.__listeners.get(listener, None)
        if not functions:
            events = set()
            self.__listeners[listener] = events
        if function: functions.add(function)


    def __del_listener(self, listener, function=None):
        if not function:
            try:
                del self.__listeners[listener]
            except: pass
        else:
            functions = self.__listeners.get(listener, None)
            if not functions: return
            try:
                functions.remove(function)
            except: pass


    def __process_ops(self):
        for op, listener, func in self.__listener_ops:
            if op == _OP_ADD: self.__add_listener(listener, func)
            else: self.__del_listener(listener, func)


