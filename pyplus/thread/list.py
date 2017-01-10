
import threading

class List(object):
    def __init__(self, *args, **kwargs):  # known special case of self._list.__init__
        self._list = list(*args, **kwargs)
        self._mutex = threading.Lock()

    def append(self, p_object):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.append, p_object)

    def count(self, value):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.count, value)

    def extend(self, iterable):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.extend, iterable)

    def index(self, *args, **kwargs):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.index, *args, **kwargs)

    def insert(self, index, p_object):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.insert, index, p_object)

    def pop(self, index=None):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.pop, index)

    def remove(self, value):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.remove, value)

    def reverse(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.reverse)

    def sort(self, *args, **kwargs):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.sort, *args, **kwargs)

    def __add__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__add__, y)

    def __contains__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__contains__, y)

    def __delitem__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__delitem__, y)

    def __delslice__(self, i, j):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__delslice__, i, j)

    def __eq__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__eq__, y)

    '''
    def __getattribute__(self, name):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__getattribute__, name)
    '''

    def __getitem__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__getitem__, y)

    def __getslice__(self, i, j):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__getslice__, i, j)

    def __ge__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__ge__, y)

    def __gt__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__gt__, y)

    def __iadd__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__iadd__, y)

    def __imul__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__imul__, y)

    def __iter__(self):  # real signature unknown; restored from __doc__
        self._mutex.acquire()
        array = [i for i in self._list]
        it = iter(array)
        self._mutex.release()
        return it

    def __len__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__len__)

    def __le__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__le__, y)

    def __lt__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__lt__, y)

    def __mul__(self, n):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__mul__, n)

    def __ne__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__ne__, y)

    def __repr__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__repr__)

    def __reversed__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__reversed__)

    def __rmul__(self, n):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__rmul__, n)

    def __setitem__(self, i, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__setitem__, i, y)

    def __setslice__(self, i, j, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__setslice__, i, j, y)

    def __sizeof__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._list.__sizeof__)


    def _pv_do(self, f, *args, **kwargs):
        #print(f)
        mutex = getattr(self, '_mutex')
        try:
            mutex.acquire()
            return f(*args, **kwargs)

        except Exception, e:
            print(e)

        finally:
            mutex.release()



if __name__ == '__main__':
    import copy
    import pickle

    l = List()
    l.append(1)
    l.count(1)
    l.extend([1,2,3])
    l.index(2)
    l.insert(1,5)
    l.pop(1)
    l.remove(2)
    l.reverse()
    l.sort()
    len(l)