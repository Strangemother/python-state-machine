
RUNNING = 'running'
CLEAR = None
CREATED = 'CREATED'

class Const(object):
    # Does the previous or current value match the new value
    EXACT = ('__EXACT__', 'Exact', )
    # Has the new value changed in a positive manner to the old valuw
    # POSITIVE = ('__POSITIVE__', 'Positive', )
    # Has the new value changed in a negative manner to the old value
    # NEGATIVE = ('__NEGATIVE__', 'Negative', )
    # Does the new value differ to the old value
    # CHANGED = ('__CHANGED__', 'Changed', )
    # Is the old value None and new value not None
    # CREATED = ('__CREATED__', 'Created', )


def register_compare(*klasses):
    '''
    Register a comparison class for use with Const.CLASS_NAME
    '''

    for klass in klasses:
        name = klass.__name__
        upper = name.upper()
        place  = '__{0}__'.format(upper)
        tuple_val = (place, name)
        setattr(Const, upper,tuple_val)
        #Const[upper] = tuple_val
