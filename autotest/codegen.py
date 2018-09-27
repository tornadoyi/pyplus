import os
from pyplus import codegen as cg
from pyplus import autotest
from pyplus.importer import import_python

def test_codegen():
    node = autotest.add('codegen')

    def gen():
        layouts = [
            cg.import_as('math', 'mt'),
            '',
            '',
            cg.pydef('add', ['x', 'y'], [
                'z = x + y',
                'return z'
            ]),
            '',
            cg.pydef('sub', ['x', 'y'], [
                'z = x - y',
                'return z'
            ]),
            '',
            '',
            cg.pyclass('TestA', [
                cg.member('__init__', ['x', 'y'], [
                    'self._x = x',
                    'self._y = y',
                ]),
                '',
                cg.getter('x', ['return self._x']),
                '',
                cg.setter('x', ['self._x = v']),
                '',
                cg.member('calculate', ['return add(self._x, self._y)'])
            ]),
            '',
            cg.pyclass('TestB', 'TestA', [
                cg.member('calculate', ['return sub(self._x, self._y)'])
            ]),
            '',
            '',
            cg.B('if __name__ == "__main__":', [
                'a = TestA(10, 5)',
                'b = TestB(10, 5)',
                'print(a.calculate())',
                'print(b.calculate())',
            ])
        ]

        code = cg.generate(layouts)

        with open('test_codegen.py', 'w') as f:
            f.write(code)

        module = import_python('test_codegen.py')
        os.remove('test_codegen.py')
        return module['TestA'](10, 5).calculate() == 15


    node.add('gen', exec=gen)
    return node


#test_codegen = test_codegen()


if __name__ == '__main__':
    pass#test_codegen()

