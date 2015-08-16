'''
A condition
'''
from base import Base
from compares import const


class ComparisonMixin(object):
    '''
    Compare two values with a comparison utility
    to denote if a change has validated.
    '''

    def compare(self, a, b, ctype=None):
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
        return comp.match(a,b)

    def get_comparison_class(self, compare):
        '''
        Return the compare class by string
        '''
        m = __import__('conditions.compares.simple', fromlist=[compare])
        # print 'module', m
        # print 'compare', compare
        k = getattr(m, compare)

        return k


class Condition(ComparisonMixin):
    '''
    A condition perpetuates changes of an object base upon
    rules applied at configuration.
    '''


    def __init__(self, node, attr, value=None, valid=None):
        '''
        A condition requires
        a node (Node|String|iterable),
        the attribute to monitor (String),
        a value to validate condition.

        Optionally `valid` callback when the condition is met

        '''
        self.watch = node
        self.field = attr
        self.target = value
        self._valid_cb = valid

    def validate(self, node, value, field):
        '''
        Validate the condition against a node and it's value.
        The self.watch should match the node, self.field matches
        member field and value should match your target.

        This does not consider dynamically generated Conditions, but the
        values passed should assist in matching attributes dynamically.
        '''
        # Checking from the node early, the value will
        # not be set yet
        # v = getattr(node, self.field)
        print 'check', value, self.target
        match = node.get_name() == self.watch and \
                field == self.field and \
                value == self.target

        if match:
            c = self.compare(value, self.target)
            if c is True and self._valid_cb:
                self._valid_cb(node, value, field)
            return True

        return False

    def __str__(self):
        s = '{0}_{1}_{2}'.format(self.watch, self.field, self.target)
        return s
