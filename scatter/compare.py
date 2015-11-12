from compares.const import Const as const


class ComparisonMixin(const):
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
