
import time
import asyncio

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
    def __init__(self, processes):
        self.__ps = processes


    @property
    def proccesses(self): return self.__ps

    @property
    def done(self):
        for p in self.__ps:
            if not p.done(): return False
        return True

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

_INTERNAL_OUTPUT_FUNCS = {'lines': _readlines, 'str': _readstr}

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


async def run_all(cmds, timeout=None, retry=0, loop=None, output=None):
    output = _get_output()
    ps = []
    for cmd in cmds: ps.append(await Process.create(cmd, timeout, retry, loop))
    mp = MutiProcesses(ps)
    await mp.wait()
    results = []
    for p in mp.proccesses:
        if p.returncode != 0:
            results.append(CmdRunError(p.cmd, p.returncode, await _readstr(p.stderr), await _readstr(p.stdout)))
        else:
            results.append(await output(p.stdout))
    return results



