from .core import *



import pkgutil
pkg = pkgutil.get_data(__package__, 'VERSION')
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()

del pkgutil