import copy


class Layout(object):
    def __init__(self, *args, **kwargs):
        self._reset(*args, **kwargs)


    def compile(self, level=0): return self._compile(level)

    def format(self, *args, **kwargs):
        cls = copy.deepcopy(self)
        cls._format(*args, **kwargs);
        return cls

    def replace(self, *args, **kwargs):
        cls = copy.deepcopy(self)
        cls._replace(*args, **kwargs);
        return cls


    def _reset(self, *args, **kwargs): raise NotImplementedError('_reset need to implement')

    def _compile(self, level): raise NotImplementedError('_compile need to implement')

    def _format(self, *args, **kwargs): raise NotImplementedError('_format need to implement')

    def _replace(self, *args, **kwargs): raise NotImplementedError('_replace need to implement')


class Line(Layout):

    def __repr__(self): return self.__str__()

    def __str__(self):
        text = ''
        for s in self.__texts: text += s
        return text

    def _reset(self, texts):
        text_list = texts if isinstance(texts, (tuple, list)) else [texts]
        self.__texts = []
        for t in text_list:
            if not isinstance(t, str): raise Exception('invalid text type {}'.format(type(t)))
            self.__texts.append(t)

    def _compile(self, level): return '\t' * level + self.__str__()

    def _format(self, *args, **kwargs): self.__texts = [t.format(*args, **kwargs) for t in self.__texts]

    def _replace(self, *args, **kwargs): self.__texts = [t.replace(*args, **kwargs) for t in self.__texts]



class Block(Layout):
    def _reset(self, headers, contents):
        self.__headers = [Line(l) if isinstance(l, str) else l for l in headers]
        self.__contents = [Line(l) if isinstance(l, str) else l for l in contents]

    def _compile(self, level):
        headers = [l.compile(level) for l in self.__headers]
        contents = []
        for l in self.__contents:
            c = l.compile(level+1)
            if isinstance(c, (tuple, list)):
                contents += c
            else:
                contents.append(c)
        return headers + contents


    def _format(self, *args, **kwargs):
        self.__headers = [l.format(*args, **kwargs) for l in self.__headers]
        self.__contents = [l.format(*args, **kwargs) for l in self.__contents]

    def _replace(self, *args, **kwargs):
        self.__headers = [l.replace(*args, **kwargs) for l in self.__headers]
        self.__contents = [l.replace(*args, **kwargs) for l in self.__contents]



class Code(Layout):
    def _reset(self, layouts):
        self.__layouts = []
        for l in layouts:
            if isinstance(l, str): self.__layouts.append(Line(l))
            elif isinstance(l, Layout): self.__layouts.append(l)
            else: raise Exception('invalid layout type {}'.format(type(l)))


    def _compile(self, level):
        lines = []
        for l in self.__layouts:
            ln = l.compile(0)
            if isinstance(ln, str):
                lines.append(ln)
            elif isinstance(ln, (tuple, list)):
                lines += ln
            else:
                raise Exception('invalid compile object {}'.format(type(ln)))
        return lines


    def _format(self, *args, **kwargs):
        self.__layouts = [l.format(*args, **kwargs) for l in self.__layouts]


    def _replace(self, *args, **kwargs):
        self.__layouts = [l.replace(*args, **kwargs) for l in self.__layouts]




def L(s): return Line(s)

def B(h, c): return Block([h], c)


