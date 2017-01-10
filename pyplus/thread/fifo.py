from queue import Queue


class FIFO(Queue):
    def __init__(self, *args, **kwargs):
        Queue.__init__(self, *args, **kwargs)

    def push(self, *args, **kwargs): Queue.append(self, *args, **kwargs)

    def appendleft(self, *args, **kwargs): raise Exception("can not support appendleft")

    def extendleft(self, *args, **kwargs): raise Exception("can not support extendleft")

    def pop(self, *args, **kwargs): return Queue.popleft(self, *args, **kwargs)

    def popleft(self, *args, **kwargs): raise Exception("can not support popleft")




if __name__ == '__main__':
    q = FIFO()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()

    print(q)

    for i in q:
        print(i)