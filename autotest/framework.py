
import copy

from pyplus import autotest
from pyplus.framework import messager, NOTIFY_AFTER_CALL, NOTIFY_BEFORE_CALL


def test_messager():
    node = autotest.add('messager')

    def test_notify():
        @messager
        class Sender():
            def test(self, x): pass

        class Receiver(object):
            def test(self, x):
                self.v = x

        v = 100
        s = Sender()
        r = Receiver()
        s.add_listener(r)
        s.test(v)
        return v == r.v

    def test_pass_messager():
        @messager(pass_messager=True)
        class Sender():
            def test(self, x): self.v = x

        class Receiver(object):
            def test(self, x, messager):
                self.v = messager.v

        v = 100
        s = Sender()
        r = Receiver()
        s.add_listener(r)
        s.test(v)
        return v == r.v


    def call_before_and_after():
        @messager(func=[('add', NOTIFY_AFTER_CALL), ('sub', NOTIFY_BEFORE_CALL)], pass_messager=True)
        class Sender():
            def __init__(self): self.v = 0
            def add(self, x): self.v += x
            def sub(self, x): self.v -= x

        class Receiver(object):
            def __init__(self): self.v = 0
            def add(self, x, messager): self.v += messager.v
            def sub(self, x, messager): self.v -= messager.v

        v = 100
        s = Sender()
        r = Receiver()
        s.add_listener(r)
        s.add(v)
        s.sub(v)
        return r.v == 0


    node.add('notify', exec=test_notify)
    node.add('pass_messager', exec=test_pass_messager)
    node.add('call_before_and_after', exec=call_before_and_after)
    return node




test_messager = test_messager()



if __name__ == '__main__':
    test_messager()

