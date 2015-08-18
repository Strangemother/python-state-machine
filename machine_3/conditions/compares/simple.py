from base import Compare

class Exact(Compare):
    '''
    check if a and b are exact
    '''
    def match(self, a, b):
        if a == b:
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
        if a < b: return True
        return False

    def match_bool(self, a, b):
        if a is False and b is True: return True
        if a is True and b is True: return True
        return False

    def match_str(self, a, b):
        return False

    def match(self, a, b):
        if type(a) == bool: v = self.match_bool(a,b)
        if type(a) in (unicode,str,): v = self.match_str(a,b)
        if type(a) in (int,float): v = self.match_num(a,b)
        return v


class Negative(Positive):

    def match_num(self, a, b):
        v = super(Negative, self).match_num(a,b)
        return (not v)

    def match_bool(self, a, b):
        v = super(Negative, self).match_bool(a,b)
        return (not v)

class Changed(Compare):

    def match(self, a, b):
        if a != b:
            return True
        return False
