import os
from pyplus import codegen as cg
from pyplus import autotest
from pyplus.importer import execute

def lines2str(lines):
    c = ''
    for ln in lines: c += ln + '\n'
    return c

def test_codegen():
    node = autotest.add('codegen')

    codes = cg.Code([
        cg.pyimport('os'),
        cg.import_as('copy', 'cp'),
        cg.from_import('collections', 'defaultdict'),
        cg.from_import_as('pyplus', 'codegen', 'cg'),
        '',
        '',
        cg.pyclass('Add', [
            cg.member('__init__', ['a', 'b'], [
                'self.__a = a',
                'self.__b = b',
            ]),
            '',
            cg.member('__call__', ['*args', '**kwargs'], [
                'return self.__a + self.__b'
            ]),
            '',
            cg.getter('a', ['return self.__a']),
            '',
            cg.setter('a', ['self.__a = v']),
            '',
        ]),
        '',
        'f = Add({x}, {y})',
        '{result} = f()',
    ])

    def format():
        nonlocal codes
        lines = codes.format(x=1, y=2, result='result').compile()
        return execute(lines2str(lines))['result'] == 3


    def replace():
        nonlocal codes
        lines = codes.replace('{x}', '1').replace('{y}', '2').replace('{result}', 'result').compile()
        return execute(lines2str(lines))['result'] == 3



    node.add('format', exec=format)
    node.add('replace', exec=replace)
    return node


test_codegen = test_codegen()


if __name__ == '__main__':
    test_codegen()

