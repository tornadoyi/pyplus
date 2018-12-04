import os
from pyplus.async import shell
from pyplus import autotest


def test_shell():
    node = autotest.add('shell')

    async def single():
        await shell.run('touch test.txt')
        await shell.run('echo 123 >> test.txt')
        await shell.run('echo abc >> test.txt')
        lines = await shell.run('cat test.txt')
        await shell.run('rm test.txt')
        return lines[0] == '123' and lines[1] == 'abc'

    async def multiple():
        await shell.run('mkdir test')
        cmds = ['touch test/{}.txt'.format(i) for i in range(3)]
        await shell.run_all(cmds)
        result = [os.path.isfile('test/{}.txt'.format(i)) for i in range(3)]
        await shell.run('rm -rf test')
        return all(result)


    node.add('single', exec=single())
    node.add('multiple', exec=multiple())
    return node


test_shell = test_shell()



if __name__ == '__main__':
    test_shell()
    import asyncio
    asyncio.get_event_loop().close()




