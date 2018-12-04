import os
import subprocess
import time
import pickle
import pwd
from functools import partial

class Process(object):
    def __init__(self, cmd, timeout=None, retry=0,
                 user=None, preexec_fn=None):
        self.__cmd = cmd
        self.__p = Process.__create_internal_subprocess(cmd,
                                                        user, preexec_fn)
        self.__timeout = timeout
        self.__retry = retry
        self.__start_time = time.time()


    @property
    def cmd(self): return self.__cmd

    @property
    def done(self): return self.__p.poll() is not None

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

    def wait(self):
        end_time = None if self.__timeout is None else self.__start_time + self.__timeout
        try:
            for i in range(self.__retry+1):
                wait_time = None if self.__timeout is None else max(0, end_time - time.time())
                code = self.__p.wait(wait_time)
                if code == 0: break
                if i < self.__retry:
                    self.__p = Process.__create_internal_subprocess(self.__cmd)

        except subprocess.TimeoutExpired:
            pass



    @staticmethod
    def __create_internal_subprocess(cmd,
                                     user=None, preexec_fn=None):
        # process user and preexec_fn
        def _preexec_func(user, preexec_fn):
            if user is not None:
                if isinstance(user, int):
                    os.setuid(user)
                elif isinstance(user, str):
                    os.setuid(pwd.getpwnam(user).pw_uid)
                else:
                    raise Exception('Invalid user {}'.format(user))

            if preexec_fn is not None: preexec_fn()
            
        return subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             preexec_fn=partial(_preexec_func, user, preexec_fn))




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

    def communicate(self, input=None):
        return [p.communicate(input) for p in self.__ps]

    def wait(self):
        for p in self.__ps: p.wait()
        return

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


def _readlines(stream): return bytes.decode(stream.read()).rstrip('\n').split('\n')

def _readstr(stream): return bytes.decode(stream.read())

def _readpickle(stream): return pickle.loads(stream.read())

def _readsingle(stream): return bytes.decode(stream.read()).replace('\n', '')

_INTERNAL_OUTPUT_FUNCS = {
    'str': _readstr,
    str: _readstr,
    'single': _readsingle,
    'lines': _readlines,
    'pickle': _readpickle
}


def _get_output(output):
    default = _readlines
    if output is None: return default
    if isinstance(output, str): return _INTERNAL_OUTPUT_FUNCS.get(output, default)
    return output


def run(cmd, timeout=None, retry=0, output=None, **kwargs):
    output = _get_output(output)
    p = Process(cmd, timeout, retry, **kwargs)
    p.wait()
    if p.returncode != 0:
        return CmdRunError(p.cmd, p.returncode, _readstr(p.stderr),  _readstr(p.stdout))
    else:
        return output(p.stdout)


def run_all(cmds, timeout=None, retry=0, output=None, **kwargs):
    output = _get_output(output)
    ps = []
    for cmd in cmds: ps.append(Process(cmd, timeout, retry, **kwargs))
    mp = MutiProcesses(ps)
    mp.wait()
    results = []
    for p in mp.proccesses:
        if p.returncode != 0:
            results.append(CmdRunError(p.cmd, p.returncode, _readstr(p.stderr), _readstr(p.stdout)))
        else:
            results.append(output(p.stdout))
    return results