
import weakref

_weaks = {} # weakref.WeakValueDictionary()

class ExtendedRef(weakref.ref):
    def __init__(self, ob, callback=None, **annotations):
        super(ExtendedRef, self).__init__(ob, callback)
        self.__counter = 0
        for k, v in annotations.iteritems():
            setattr(self, k, v)

    def __call__(self):
        """Return a pair containing the referent and the number of
        times the reference has been called.
        """
        ob = super(ExtendedRef, self).__call__()
        if ob is not None:
            self.__counter += 1
            ob = (ob, self.__counter)
        return ob

def add_weak(p_ref, key, value):
    '''
    Add a reference to the key context of p_ref parent
    Returned is the refere
    '''
    r = id(p_ref)
    i = '{0}_{1}'.format(r, key)
    _weaks[i] = value
    return i

def get_weak(p_ref=None, key=None):
    if key is not None and p_ref is None:
        if key in _weaks:
            return _weaks[key]
        else:
            return None
    r = id(p_ref)
    i = '{0}_{1}'.format(r, key)
    if i in _weaks:
        return _weaks[i]

