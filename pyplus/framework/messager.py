import inspect
from collections import OrderedDict
from functools import partial


NOTIFY_BEFORE_CALL = 0

NOTIFY_AFTER_CALL = 1

_OP_ADD = 0
_OP_DEL = 1



class Messager(object):
    def __init__(self, obj, messages, pass_messager=False):
        self.__o = obj
        self.__messages = {}
        self.__kwargs = {'messager': self} if pass_messager else {}

        self.__listeners = OrderedDict()
        self.__listener_ops = []
        self.__lock = False

        # reset messages
        for k, v in messages.items():
            wrap_f, core_f = v
            self.__messages[k] = partial(wrap_f, self, self.__o, core_f, k)



    def __getattr__(self, item):
        f = self.__messages.get(item, None)
        if f: return f
        return getattr(self.__o, item)



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



    def _call_before(self,  obj, function, fname, *args, **kwargs):
        self.__notify(fname, *args, **kwargs)
        return function(obj, *args, **kwargs)

    def _call_after(self,  obj, function, fname, *args, **kwargs):
        result = function(obj, *args, **kwargs)
        self.__notify(fname, *args, **kwargs)
        return result



    def __notify(self, fname, *args, **kwargs):
        # notify
        self.__lock = True
        for l, functions in self.__listeners.items():
            if len(functions) > 0 and (fname not in functions): continue
            f = getattr(l, fname, None)
            if not f: continue
            f(*args, **kwargs, **self.__kwargs)
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



def messager(type=None, **kwargs):

    def create(type):
        messages = kwargs.get('func', None)
        pass_messager = kwargs.get('pass_messager', False)

        # generate message dict
        message_dict = {}
        if messages:
            for msg in messages:
                if isinstance(msg, tuple): fname, call_type = msg
                elif isinstance(msg, str): fname, call_type = msg, NOTIFY_AFTER_CALL
                else: raise Exception('Invalid message item')
                f = getattr(type, fname, None)
                if not f: continue
                call = Messager._call_before if call_type == NOTIFY_BEFORE_CALL else Messager._call_after
                message_dict[fname] = (call, f)
        else:
            for fname, f in type.__dict__.items():
                if not inspect.isfunction(f): continue
                if fname.startswith('__') and fname.endswith('__'): continue
                message_dict[fname] = (Messager._call_after, f)

        def instantiate(*args, **kwargs):
            o = type(*args, **kwargs)
            return Messager(o, message_dict, pass_messager)

        return instantiate


    return create(type) if type else create


