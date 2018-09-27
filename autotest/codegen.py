
from pyplus import codegen as cg


if __name__ == '__main__':

    layouts = [
        cg.import_as('numpy', 'np'),
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

    with open('codegen.py', 'w') as f:
        f.write(code)