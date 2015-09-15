from root import *

import sys, os


def write_sys(path=None):
    '''
    Append the directory to the current sys path to ensure
    loading deep modules can still import root components.

    This method is run from init or main
    '''
    p = __file__ if path is None else path
    d = os.path.dirname( os.path.abspath(p))
    print 'write_sys', d
    sys.path.insert(0, d)


write_sys()
