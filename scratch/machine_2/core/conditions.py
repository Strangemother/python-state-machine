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
        m = __import__('core.compares.simple', fromlist=[compare])
        # print 'module', m 
        # print 'compare', compare
        k = getattr(m, compare)

        return k


class Condition(Base, ComparisonMixin):
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

    def valid(self):
        '''
        Is this condition valid
        '''
        vs = self._validate()
        for node in vs:
            val = vs[node]
            if val == False: return False

        return True

    def get_nodes(self):
        '''
        return a list of Nodes retrieved from the machine using the
        `watch` attr. Each item in the `watch` iterable will be 
        parsed into a Node type.
        '''
        if isinstance(self.watch, (tuple, list,) ) is not True:
            # create iterable
            return [self.watch]
        # is iterable
        return self.watch

    def _validate(self, nodes=None, field=None, ctype=None):
        '''
        validate the condition against the assigned node.
        Returns boolean

        Provide nodes as a node, a list of nodes or a string for 
        network aquisition.

        ctype defines the comapre utility to use for validation
        '''
        nodes = nodes or self.get_nodes()
        # attr of the node to inspect
        field = field or self.field
        # the value to target.
        value = self.target

        if len(nodes) == 0:
            return (False, 'no machine node %s' % self.watch)

        r = {};
        # print 'nodes', nodes
        for node in nodes:
            # current value
            v = node.get(field)
            # print 'node:', v, 'cache', cv, 'ctype', ctype
            c = self.compare(v, value, ctype)
            r.update({ node: c })
            # import pdb;pdb.set_trace()  

        return r
