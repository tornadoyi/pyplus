import os
import asyncio
from pyplus.async import shell


async def test_shell():
    # base shell test
    await shell.run('touch test.txt')
    await shell.run('echo 123 >> test.txt')
    await shell.run('echo abc >> test.txt')
    lines = await shell.run('cat test.txt')
    await shell.run('rm test.txt')
    assert lines[0] == '123' and lines[1] == 'abc'


    # mutiple shell test
    await shell.run('mkdir test')
    cmds = [
        'touch test/1.txt',
        'touch test/2.txt',
        'touch test/3.txt',
    ]
    await shell.run_all(cmds)
    assert os.path.isfile('test/1.txt')
    assert os.path.isfile('test/2.txt')
    assert os.path.isfile('test/3.txt')
    await shell.run('rm -rf test')



async def test():
    await test_shell()




loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()
