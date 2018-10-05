
import time
import asyncio
import pickle

class Process(object):
    def __init__(self, cmd, process, timeout, retry, loop):
        self.__cmd = cmd
        self.__p = process
        self.__timeout = timeout
        self.__retry = retry
        self.__loop = loop
        self.__done_future = asyncio.Future()


    @staticmethod
    async def create(cmd, timeout=None, retry=0, loop=None):
        if loop is None: loop = asyncio.get_event_loop()
        _p = await Process.__create_internal_subprocess(cmd, loop)
        p = Process(cmd, _p, timeout, retry, loop)
        loop.create_task(p.__supervise())
        return p

    @property
    def cmd(self): return self.__cmd

    @property
    def done(self): return self.__p.returncode is not None

    @property
    def pid(self): return self.__p.pid()

    @property
    def returncode(self): return self.__p.returncode

    @property
    def stdin(self): return self.__p.stdin

    @property
    def stdout(self): return self.__p.stdout

    @property
    def stderr(self): return self.__p.stderr

    def communicate(self, input=None): return self.__p.communicate(input)

    def send_signal(self, signal): return self.__p.send_signal(signal)

    def terminate(self): return self.__p.terminate()

    def kill(self): return self.__p.kill()

    def wait(self, ): return self.__done_future


    async def __supervise(self):
        start_time = time.time()
        end_time = None if self.__timeout is None else start_time + self.__timeout
        try:
            for i in range(self.__retry + 1):
                wait_time = None if self.__timeout is None else max(0, end_time - time.time())
                code = await asyncio.wait_for(self.__p.wait(), wait_time, loop=self.__loop)
                if code == 0: break
                if i < self.__retry:
                    self.__p = await self.__create_internal_subprocess(self.__cmd, self.__loop)

        except asyncio.TimeoutError:
            pass

        self.__done_future.set_result(True)



    @staticmethod
    async def __create_internal_subprocess(cmd, loop):
        return await  asyncio.create_subprocess_shell(cmd,
                                                      stdin=asyncio.subprocess.PIPE,
                                                      stdout=asyncio.subprocess.PIPE,
                                                      stderr=asyncio.subprocess.PIPE,
                                                      loop=loop)



class MutiProcesses(object):
    def __init__(self, processes, loop=None):
        self.__loop = asyncio.get_event_loop() if loop is None else loop
        self.__ps = []
        self.__done_callbacks = []
        self.__all_done_future = asyncio.Future()

        # load processes
        for p in processes: self.add_process(p)


    @property
    def proccesses(self): return self.__ps

    @property
    def done(self):
        for p in self.__ps:
            if not p.done: return False
        return True

    @property
    def runnings(self):
        c = 0
        for p in self.__ps:
            if not p.done(): c += 1
        return c

    async def communicate(self, input=None):
        if len(self.__ps) == 0: return []
        dones, _ = await asyncio.wait([p.communicate(input) for p in self.__ps])
        return [d.result() for d in dones]

    async def wait(self):
        if len(self.__ps) == 0: return []
        dones, _ = await asyncio.wait([p.wait() for p in self.__ps])
        return [d.result() for d in dones]

    def send_signal(self, signal): return [p.send_signal(signal) for p in self.__ps]

    def terminate(self): return [p.terminate() for p in self.__ps]

    def kill(self): return [p.kill() for p in self.__ps]

    def add_process(self, p):

        async def __supervise(i):
            p = self.__ps[i]
            await p.wait()
            self.__on_process_done(i)

        # save and supervise
        self.__ps.append(p)
        self.__loop.create_task(__supervise(len(self.__ps)-1))

        # reset done future
        if self.__all_done_future.done(): self.__all_done_future = asyncio.Future()


    def add_process_done_callback(self, cb): self.__done_callbacks.append(cb)

    def remove_process_done_callback(self, cb): self.__done_callbacks = [c for c in self.__done_callbacks if cb != c]

    def __on_process_done(self, i):
        # callback
        p = self.__ps[i]
        for cb in self.__done_callbacks: cb(p)

        # check all done
        if self.done: self.__all_done_future.set_result(True)







class CmdRunError(BaseException):
    def __init__(self, cmd, code, error, output):
        super(CmdRunError, self).__init__()
        self.__cmd = cmd
        self.__code = code
        self.__error = error
        self.__output = output

    @property
    def cmd(self): return self.__cmd

    @property
    def code(self): return self.__code

    @property
    def error(self): return self.__error

    def __str__(self):
        return 'Command run failed:' + '\n'\
               '    Error code: {}'.format(self.__code) + '\n'\
               '    Error: {}'.format(self.__error) + '\n' + \
               '    Ouput: {}'.format(self.__output) + '\n' + \
               '    Command: {}'.format(self.__cmd) + '\n'

    def __repr__(self): self.__str__()



async def _readlines(stream): return bytes.decode(await stream.read()).rstrip('\n').split('\n')

async def _readstr(stream): return bytes.decode(await stream.read())

async def _readpickle(stream): return pickle.loads(await stream.read())


_INTERNAL_OUTPUT_FUNCS = {'lines': _readlines, 'str': _readstr, 'pickle': _readpickle}

def _get_output(output):
    default = _readlines
    if output is None: return default
    if isinstance(output, str): return _INTERNAL_OUTPUT_FUNCS.get(output, default)
    return output


async def run(cmd, timeout=None, retry=0, loop=None, output=None):
    output = _get_output(output)
    p = await Process.create(cmd, timeout, retry, loop)
    await p.wait()
    if p.returncode != 0:
        return CmdRunError(p.cmd, p.returncode, await _readstr(p.stderr), await _readstr(p.stdout))
    else:
        return await output(p.stdout)


async def run_all(cmds, timeout=None, retry=0, loop=None, output=None, max_parallel=None):
    output = _get_output(output)
    loop = asyncio.get_event_loop() if loop is None else loop
    if max_parallel is None: max_parallel = len(cmds)

    mp = MutiProcesses([])
    cur_index, fill_future = 0, asyncio.Future()

    process_done_callback = None

    async def _fill_processes():
        nonlocal cur_index

        max_fill = max_parallel - mp.runnings
        dst_index = min(len(cmds), cur_index + max_fill)
        for i in range(cur_index, dst_index):
            mp.add_process(await Process.create(cmds[i], timeout, retry, loop))

        # reset cur index
        cur_index = dst_index
        if cur_index >= len(cmds):
            fill_future.set_result(True)
            mp.remove_process_done_callback(process_done_callback)

    process_done_callback = lambda *args: loop.create_task(_fill_processes())

    # listen process done
    mp.add_process_done_callback(process_done_callback)

    # start init processes
    await _fill_processes()

    # wait fill
    await fill_future

    # wait all processes done
    await mp.wait()

    # collect results
    results = []
    for p in mp.proccesses:
        if p.returncode != 0:
            results.append(CmdRunError(p.cmd, p.returncode, await _readstr(p.stderr), await _readstr(p.stdout)))
        else:
            results.append(await output(p.stdout))
    return results





