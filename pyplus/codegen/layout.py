
class Layout(object):

    def compile(self): return self.__compile__()

    def __compile__(self): raise NotImplementedError('__compile__ need to implement')




class Flat(Layout):
    def __init__(self, layouts):
        self._layouts = layouts if isinstance(layouts, (tuple, list)) else [layouts]

    def append(self, ln): self._layouts.append(ln)

    def __compile__(self):
        layouts = []
        for c in self._layouts:
            if isinstance(c, (str, Layout)): layouts.append(c)
            else: raise Exception('invalid layout type: {}'.format(type(c)))
        return layouts


class Block(Flat):
    def __init__(self, headers, layouts):
        super(Block, self).__init__(layouts)
        self._headers = headers if isinstance(headers, (tuple, list)) else [headers]


    def __compile__(self):
        headers = []
        for h in self._headers:
            if not isinstance(h, (str, Line)):
                raise Exception('invalid layout type: {}, type must be str or Line'.format(type(h)))
            headers.append(h)
        return headers, super(Block, self).__compile__()


class Line(Layout):
    def __init__(self, code):
        self._code =  code

    def __repr__(self): self.__str__()

    def __str__(self): return self._code

    def __compile__(self): return self.__str__()


def L(s): return Line(s)

def B(h, c): return Block(h, c)




def generate(layouts):
    lines = [];
    _generate(layouts, lines, 0)
    code = ''
    for i in range(len(lines)):
        code += lines[i]
        if i < len(lines)-1: code += '\n'
    return code



def _generate(layouts, lines=[], tab_count=0):
    tabs = _tab(tab_count)
    for l in layouts:
        t = type(l)
        if t == str: lines.append(tabs + l)
        elif isinstance(l, Line): lines.append(tabs + l.compile())
        elif isinstance(l, Block):
            headers, contents = l.compile()
            _generate(headers, lines, tab_count)
            _generate(contents, lines, tab_count+1)
        elif isinstance(l, Flat):
            contents = l.compile()
            _generate(contents, lines, tab_count)

def _tab(c):
    s = ''
    for i in range(c): s += '\t'
    return s
