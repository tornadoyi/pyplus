
from collections import deque
import threading



class Queue(object):
    def __init__(self, *args, **kwargs):
        self._queue = deque(*args, **kwargs)
        self._mutex = threading.Lock()

    def append(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.append, *args, **kwargs)

    def appendleft(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.appendleft, *args, **kwargs)

    def clear(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.clear, *args, **kwargs)

    def count(self, value): # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.count, value)

    def extend(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.extend, *args, **kwargs)

    def extendleft(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.extendleft, *args, **kwargs)

    def pop(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.pop, *args, **kwargs)

    def popleft(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.popleft, *args, **kwargs)

    def remove(self, value): # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.remove, value)

    def reverse(self): # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.reverse)

    def rotate(self, *args, **kwargs): # real signature unknown
        return self._pv_do(self._queue.rotate, *args, **kwargs)

    def __copy__(self, *args, **kwargs):  # real signature unknown
        return self._pv_do(self._queue.__copy__, *args, **kwargs)

    def __delitem__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__delitem__, y)

    def __eq__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__eq__, y)

    '''
    def __getattribute__(self, name):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__getattribute__, name)
    '''

    def __getitem__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__getitem__, y)

    def __ge__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__ge__, y)

    def __gt__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__gt__, y)

    def __iadd__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__iadd__, y)

    def __iter__(self):  # real signature unknown; restored from __doc__
        self._mutex.acquire()
        array = [i for i in self._queue]
        it = iter(array)
        self._mutex.release()
        return it

    def __len__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__len__)

    def __le__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__le__, y)

    def __lt__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__lt__, y)

    def __ne__(self, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__ne__, y)

    def __reduce__(self, *args, **kwargs):  # real signature unknown
        return self._pv_do(self._queue.__reduce__, *args, **kwargs)

    def __repr__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__repr__)

    def __reversed__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__reversed__)

    def __setitem__(self, i, y):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__setitem__, i, y)

    def __sizeof__(self):  # real signature unknown; restored from __doc__
        return self._pv_do(self._queue.__sizeof__)


    def _pv_do(self, f, *args, **kwargs):
        #print(f)
        mutex = getattr(self, '_mutex')
        try:
            mutex.acquire()
            return f(*args, **kwargs)

        except Exception as e:
            print(e)

        finally:
            mutex.release()


if __name__ == '__main__':
    import copy
    import pickle

    q = Queue()
    q.append(1)
    q.appendleft(2)
    q.clear()
    q.extend([6,7,8,9])
    q.extendleft([1,2,3,4,5])
    q.pop()
    q.popleft()
    q.remove(2)
    q.reverse()
    q.rotate()
    q2 = copy.copy(q)

    del q2[2]
    q == q2
    q[2]
    q >= q2
    q > q2
    q += q2
    len(q)
    q <= q2
    q < q2
    q != q2
    reversed(q)
    q[2] = 10
    pickle.dumps(q)

    print(q)

    for i in q:
        print(i)