from .fifo import FIFO
from .list import List
import threading
import time


class Pool(object):
    def __init__(self, init_thread_count, max_thread_count):
        self._max_thread_count = max_thread_count
        self._jobs = FIFO()
        self._finish_jobs = FIFO()
        self._threads = List()
        self._idle_threads = FIFO()
        self._mutex = threading.Lock()

    def destroy(self):
        self._mutex.acquire()
        for t in self._threads:
            t.exit()

        self._jobs.clear()
        self._finish_jobs.clear()
        self._threads = List()
        self._idle_threads.clear()
        self._mutex.release()



    @property
    def thread_count(self): return len(self._threads)

    @property
    def max_thread_count(self): return self._max_thread_count

    @property
    def idle_thread_count(self): return len(self._idle_threads)

    @property
    def wait_job_count(self): return len(self._jobs)

    def run(self, thread_func, *args, **kwargs):
        # push job
        job = Job(thread_func, *args, **kwargs)
        self._jobs.push(job)

        # create threads
        need_thread_count = len(self._jobs) - len(self._idle_threads)
        can_apply_thread_count = self._max_thread_count - len(self._threads)
        create_thread_count = min(need_thread_count, can_apply_thread_count)
        for i in xrange(create_thread_count):
            self._create_thread()

        return job


    def update(self):
        # dispatch jobs
        self._dispatch()

        # callback finish jobs
        self._mutex.acquire()
        for j in self._finish_jobs:
            if j.error != None:
                if j.error_callback == None: continue
                j.error_callback(j.error)

            else:
                if j.finish_callback == None: continue
                j.finish_callback(j.ret)

        self._finish_jobs.clear()
        self._mutex.release()


    def _create_thread(self):
        self._mutex.acquire()

        # create thread
        t = Thread(len(self._threads), self)
        t.start()

        # add to list
        self._threads.append(t)
        self._idle_threads.push(t)

        self._mutex.release()


    def _dispatch(self):
        # check
        if len(self._jobs) <= 0 or len(self._idle_threads) == 0: return

        # dispatch
        self._mutex.acquire()

        while len(self._jobs) > 0 and len(self._idle_threads) > 0:
            # pop job and thread
            j = self._jobs.pop()
            t = self._idle_threads.pop()

            # awake thread
            t.run_job(j)

        self._mutex.release()


    def finish_job(self, t):
        self._mutex.acquire()
        self._idle_threads.push(t)
        self._finish_jobs.push(t.job)
        self._mutex.release()



class Thread(threading.Thread):
    def __init__(self, index, pool, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self._index = index
        self._pool = pool
        self._event = threading.Event()
        self._exit = False
        self._job = None
        self._finish = True


    @property
    def index(self): return self._index

    @property
    def idle(self): return self._event.is_set() == False

    @property
    def job(self): return self._job

    def run_job(self, job):
        assert self.idle
        self._job = job
        self._finish = False
        self._event.set()

    def exit(self):
        self._exit = True
        self._event.set()


    def run(self):
        # wait
        self._event.wait()

        while not self._exit:
            # check job function
            if not self._finish:
                try:
                    self._job.ret = self._job.func(*self._job.args, **self._job.kwargs)

                except Exception as e:
                    self._job.error = e

            # call back
            self._finish_job()

            # check exit
            if self._exit: break

            self._event.clear()
            self._event.wait()


    def _finish_job(self):
        self._finish = True
        self._pool.finish_job(self)




class Job(object):
    def __init__(self, thread_func, *args, **kwargs):
        self.func = thread_func
        self.args = args
        self.kwargs = kwargs

        self.error = None
        self.ret = None

        self.finish_callback = None
        self.error_callback = None



if __name__ == '__main__':

    def test_func(i, j):
        if i % 10 == 0:
            raise Exception('only test error')
        else:
            print('index func {0} {1}'.format(i, j))

        return (1,2,3)


    def print_error(error):
        print(error)


    pool = Pool(5, 10)

    for i in xrange(1, 100):
        j = pool.run(test_func, i, i + 1)
        j.error_callback = print_error


    while pool.wait_job_count > 0:
        pool.update()
        time.sleep(0.01)

    print('destory pool')
    pool.destroy()
    print('finish')