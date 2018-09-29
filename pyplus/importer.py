from __future__ import absolute_import, division, print_function


from importlib import import_module


def import_python(path):
    with open(path, 'r') as f:
        code = f.read()
    m = {}
    exec(code, m)
    return m



def execute(code):
    m = {}
    exec(code, m)
    return m



def import_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj





