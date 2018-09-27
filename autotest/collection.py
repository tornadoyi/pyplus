
import copy

from pyplus.collection import qdict
from pyplus import autotest


def test_qdict():
    node = autotest.add('qdict')

    d = qdict(a=1, b=2, c=3)
    class Test(qdict):
        pass

    def pickle():
        import pickle
        en = pickle.dumps(d)
        de = pickle.loads(en)
        return de == d

    def inherit():
        t = Test(x=1, y=2)
        ct = copy.deepcopy(t)
        return type(ct) == type(t)

    def merge():
        t = Test(x=1, y=2)
        empty = Test()
        empty.merge(t)
        return empty == t


    node.add('pickle', exec=pickle)
    node.add('inherit', exec=inherit)
    node.add('merge', exec=merge)
    return node




test_qdict = test_qdict()



if __name__ == '__main__':
    test_qdict()

