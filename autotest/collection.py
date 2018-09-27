
import copy

from pyplus.collection import qdict


def test_qdict():
    d = qdict(a=1, b=2, c=3)

    # test pickle
    import pickle
    en = pickle.dumps(d)
    de = pickle.loads(en)
    print(de == d)

    # test inherit
    class Test(qdict):
        pass

    t = Test(x=1, y=2)
    ct = copy.deepcopy(t)
    print(type(ct) == type(t))

    # merge
    empty = Test()
    empty.merge(t)
    print(empty == t)



def test():
    test_qdict()

