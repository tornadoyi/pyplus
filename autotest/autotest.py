import os
from pyplus import autotest


def test():
    test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cases')
    manager = autotest.Manager('Test pyplus')
    manager.scan(test_path, exclude=[os.path.basename(__file__)])
    manager()

if __name__ == '__main__':
    test()