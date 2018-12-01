import os
import copy

from pyplus.subprocess import shell
from pyplus import autotest


def test_shell():
    node = autotest.add('shell')

    def single():
        shell.run('touch test.txt')
        shell.run('echo 123 >> test.txt')
        shell.run('echo abc >> test.txt')
        lines = shell.run('cat test.txt')
        shell.run('rm test.txt')
        return lines[0] == '123' and lines[1] == 'abc'

    def multiple():
        shell.run('mkdir test')
        cmds = ['touch test/{}.txt'.format(i) for i in range(3)]
        shell.run_all(cmds)
        result = [os.path.isfile('test/{}.txt'.format(i)) for i in range(3)]
        shell.run('rm -rf test')
        return all(result)


    node.add('single', exec=single)
    node.add('multiple', exec=multiple)
    return node


test_shell = test_shell()



if __name__ == '__main__':
    test_shell()

