from const import register_compare, Const as const

class CodeRegister(type):
    def __init__(cls, name, bases, dct):
        # register_code(cls, name)
        register_compare(cls)
        super(CodeRegister, cls).__init__(name, bases, dct)


class Valid(object):
    '''
    validity statement for a local node.

        >>> v=scatter.conditions.Valid(1)
        >>> v.match(3)
        False
        >>> v.match(1)
        True

    '''
    __metaclass__ = CodeRegister

    def __init__(self, value=None):
        # Value to match on call
        self.value = value

    def match(self, a, b=None, **kw):
        '''
        Match the value with the internal value.
        (b) value can be passed if self.value is None or
        to override
        '''
        b = b or self.value
        return (a == b)


class Compare(Valid):
    '''
    Compare two values with a comparison utility
    to denote if a change has validated.
    '''

    def compare(self, node, current, incoming, ctype=None, value=None):
        '''
        compare 'a' against 'b' for a comparison of `ctype`
        by defauly ctype will compare for an exact match
        '''

        if ctype is None:
            ctype = const.EXACT
        # internal importer for core.compares.simple.
        Comp = self.get_comparison_class(ctype)
        # new class of
        comp = Comp(self)
        # perform comparison
        match_val = value or current
        # We chack the existing existing what we should have.
        return comp.match(incoming, match_val, node=node, current=current)

    def get_comparison_class(self, compare):
        '''
        Return the compare class by string
        '''
        import conditions
        # m = __import__('scatter.compares.simple', fromlist=[compare])
        m = conditions
        # print 'module', m
        # print 'compare', compare

        k = getattr(m, compare)
        return k

    @staticmethod
    def args(node, value, field, const):
        '''
        return arguments to fit, condition.compare method
        '''
        res = [node, value, getattr(node, field), const]
        return res

    def __init__(self, condition=None):
        self.condition = condition


class Exact(Compare):
    '''
    check if a and b are exact
    '''
    def match(self, a, b, **kw):
        if a == b:
            return True
        return False


class Created(Compare):
    '''
    Match a as not None and b as None
    '''
    def match(self, a, b, **kw):
        return (a is not None) and (b is None)


class Changed(Compare):

    def match(self, a, b, **kw):
        # print 'Condition Changed', a,b
        if a != b:
            return True
        return False


class Positive(Compare):
    '''
    Determin if a as changes in a positive direction to b
    Cannot compare string

    Boolean:

    False > True  > True
    True > True   > True
    False > False > False
    True > False  > False

    Int/Float

    0 > + > True
    0 > - > False
    0 > 0 > False

    This active compare will compare against it's last stored cache.
    Each time the compare is called, the value is stored for the
    next procedure to inspect
    '''

    def match_num(self, a, b):
        if a > b:
            r = True
        else:
            r = False
        # print 'Positive matching a, b', a, b, '==', r
        return r

    def match_bool(self, a, b):
        if a is False and b is True: return True
        if a is True and b is True: return True
        return False

    def match_str(self, a, b):
        return False

    def match(self, a, b, **kw):
        if type(a) == bool: v = self.match_bool(a,b)
        if type(a) in (unicode, str,): v = self.match_str(a, b)
        if type(a) in (int, float): v = self.match_num(a, b)
        return v


class Negative(Positive):

    def match_num(self, a, b):
        v = super(Negative, self).match_num(a,b)
        return (not v)

    def match_bool(self, a, b):
        v = super(Negative, self).match_bool(a,b)
        return (not v)


# register_compare(Exact, Created, Changed, Positive, Negative)
