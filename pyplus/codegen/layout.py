import copy

class Layout(object):
    def __init__(self, *args, **kwargs):
        self.__reset__(*args, **kwargs)

    def compile(self): return self.__compile__()

    def format(self, **kwargs):
        cls = copy.deepcopy(self)
        cls.__formater__(**kwargs);
        return cls

    def clear(self, tag):
        cls = copy.deepcopy(self)
        cls.__clear__(tag);
        return cls


    def __reset__(self, *args, **kwargs): raise NotImplementedError('__reset__ need to implement')

    def __compile__(self): raise NotImplementedError('__compile__ need to implement')

    def __formater__(self, **kwargs): raise NotImplementedError('__format__ need to implement')

    def __clear__(self, tag): raise NotImplementedError('__clear__ need to implement')



class Line(Layout):
    def __repr__(self): self.__str__()

    def __str__(self):
        text = ''
        for s in self.__texts: text += s
        return text

    def replace(self, *args, **kwargs):
        self.__texts = [t.replace(*args, **kwargs) for t in self.__texts]
        return self


    def __reset__(self, texts):
        text_list = texts if isinstance(texts, (tuple, list)) else [texts]
        self.__texts = []
        for t in text_list:
            if isinstance(t, str): self.__texts.append(t)
            else: raise Exception('invalid text type {}'.format(type(t)))

    def __compile__(self): return self.__str__()

    def __formater__(self, **kwargs):
        for i in range(len(self.__texts)):
            self.__texts[i] = self.__texts[i].format(**kwargs)


class Flat(Layout):
    def __iter__(self): return iter(self.__layouts)

    def __reset__(self, layouts):
        layout_list = layouts if isinstance(layouts, (tuple, list)) else [layouts]
        self.__layouts = []
        for l in layout_list:
            if isinstance(l, Layout): self.__layouts.append(l)
            elif isinstance(l, str): self.__layouts.append(Line(l))
            else: raise Exception('invalid layout type {}'.format(type(l)))


    def __compile__(self): return self.__layouts

    def __formater__(self, **kwargs):
        for i in range(len(self.__layouts)): self.__layouts[i] = self.__layouts[i].format(**kwargs)

    def __clear__(self, tag):
        layouts = []
        for i in range(len(self.__layouts)):
            l = self.__layouts[i]
            if isinstance(l, Line):
                if str(l) == tag:
                    continue
                else:
                    l = l.replace(tag, '')
            else:
                l.__clear__(tag)
            layouts.append(l)
        self.__layouts = layouts




class Block(Layout):
    def __reset__(self, headers, contents):
        self.__headers = Flat(headers)
        self.__contents = Flat(contents)

    def __compile__(self): return self.__headers, self.__contents

    def __formater__(self, **kwargs):
        self.__headers.__formater__(**kwargs)
        self.__contents.__formater__(**kwargs)

    def __clear__(self, tag):
        self.__headers.__clear__(tag)
        self.__contents.__clear__(tag)




def L(s): return Line(s)

def B(h, c): return Block(h, c)

def F(c): return Flat(c)




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
