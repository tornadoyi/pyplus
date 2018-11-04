
import copy

from pyplus import autotest
from pyplus.framework import Messager


def test_messager():
    node = autotest.add('messager')

    class Data(object):
        def __init__(self):
            self.value = 0

    def test_notify():
        class Sender(Messager):
            def test(self): self.notify('test', Data())

        class Receiver(object):
            def __init__(self, sender):
                self.value = 0
                sender.add_listener(self)

            def test(self, data, *args, **kwargs):
                self.value = data.value
                data.value += 1

        s = Sender()
        r1 = Receiver(s)
        r2 = Receiver(s)
        s.test()
        return (r1.value, r2.value) == (0, 1)


    def del_listener():
        class Sender(Messager):
            def test(self): self.notify('test', Data())

        class Receiver(object):
            def __init__(self, sender, max_call):
                self.value = 0
                self.max_call = max_call
                self.sender = sender
                sender.add_listener(self)

            def test(self, data, *args, **kwargs):
                self.value += 1
                if self.value < self.max_call: return
                self.sender.del_listener(self)

        max_calls = [i for i in range(1, 11)]
        s = Sender()
        rs = [Receiver(s, i) for i in max_calls]
        for i in range(100): s.test()
        true_calls = 0
        recv_calls = 0
        for i in max_calls: true_calls += i
        for r in rs: recv_calls += r.value
        return true_calls == recv_calls



    node.add('notify', exec=test_notify)
    node.add('del listener', exec=del_listener)
    return node




test_messager = test_messager()



if __name__ == '__main__':
    test_messager()

