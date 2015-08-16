import unittest
from ..core import Node, Condition
from ..core.compares.simple import Exact
from ..core.compares.base import Compare 
from ..core.compares.const import *


class TestNode(Node):
    """TestNode"""

    foo = 'bar'
    bar = 2
    color = 'red'

    def __init__(self):
        super(TestNode, self).__init__()


class TestCompare(unittest.TestCase):
    
    def setUp(self):
       self.n = TestNode()
    
    def test_compare_init(self):
        '''
        new compare should store a passed condition 
        '''
        cond = Condition(None, None)
        c = Compare(cond)
        self.assertEqual(c.condition, cond)

    def test_equal(self):
        '''
        Test equal compare
        '''
        self.n.bar = 2
        cond = Condition(self.n, 'foo', EXACT)
        c = Compare(cond)
        c.match(self.n.bar, 2)

    def test_positive(self):
        self.n.bar = 2
        cond = Condition(self.n, 'bar', POSITIVE)
        c = Compare(cond)
        self.assertFalse(c.match(self.n.bar, 3))
        self.n.bar = 1
        self.assertFalse(c.match(self.n.bar, 2))

        self.n.bar = 3
        self.assertTrue(c.match(self.n.bar, 3))


class TestConditions(unittest.TestCase):

    def setUp(self):
       self.n = TestNode()
    

    def test_valid(self):
        '''
        A condition validity should be boolean false
        by default
        '''
        c = Condition(self.n, 'foo')
        self.assertFalse(c.valid())

    def test_init_node(self):
        field = 'on'
        name = 'generic'
        other = 'other'
        valid = (list, tuple,)
        value = False
        n = Node()
        c = range(7)

        def vcb():
            pass

        c[0] = Condition(name, field)

        self.assertEqual(c[0].watch, name)
        self.assertEqual(c[0].field, field)
        self.assertIsNone(c[0].target)
        self.assertIsNone(c[0]._valid_cb)
        
        c[1] = Condition(name, field, value)

        self.assertEqual(c[1].watch, name)
        self.assertEqual(c[1].field, field)
        self.assertEqual(c[1].target, value)
        
        c[2] = Condition( [name, other]  , field)
            
        self.assertEqual(c[2].field, field)
        self.assertIsNone(c[2].target)
        self.assertEqual(c[2].watch, [name, other])
        self.assertTrue( isinstance(c[2].watch, valid) )
        
        c[3] = Condition( (name, other,) , field)

        self.assertEqual(c[3].watch, (name, other,))
        self.assertEqual(c[3].field, field)
        self.assertIsNone(c[3].target)
        self.assertTrue( isinstance(c[3].watch, valid) )
        
        c[4] = Condition( (name, other,) , field, value)
        
        self.assertEqual(c[4].field, field)
        self.assertIsNotNone(c[4].target)
        self.assertEqual(c[4].watch, (name, other,) )
        self.assertTrue( isinstance(c[4].watch, valid) )
        self.assertEqual(c[4].target, value )
        
        c[5] = Condition( (name, other,) , field, value, valid=vcb)

        self.assertEqual(c[5].watch, (name, other, ))
        self.assertEqual(c[5].field, field)
        self.assertEqual(c[5].target, value)
        self.assertEqual(c[5]._valid_cb, vcb)

        
        c[6] = Condition( (name, other,) , field, valid=vcb)
        
        self.assertEqual(c[6].watch, (name, other, ))
        self.assertEqual(c[6].field, field)
        self.assertIsNone(c[6].target)
        self.assertEqual(c[6]._valid_cb, vcb)
    
    def test_get_nodes(self):
        ''' can get all nodes as a list using 
        the get_attrs method'''
        c = Condition(self.n, 'foo')

        self.assertEqual( c.get_nodes() , [self.n])

    def test_get_comparion_class(self):
        '''
        should return a class based upon it's name 
        '''
        name = 'Exact'
        c = Condition(self.n, 'foo')
        kl = c.get_comparison_class(name)
        n = kl().__class__.__name__
        self.assertEqual(name, n)

    def test_compare_validate(self):
        '''
        Comparison should run with two arguments and 
        a compare utility
        '''
        c = Condition(self.n, 'foo')
        cv = c.compare(1,1, EXACT)
        self.assertTrue(cv)
        cv = c.compare(12,1, EXACT)
        self.assertFalse(cv)

        c = Condition(self.n, 'foo')
        # Should default to exact match
        cv = c.compare(10,10)
        self.assertTrue(cv)

        cv = c.compare('wibble', 'wibble')
        self.assertTrue(cv)

        cv = c.compare(10,1)
        self.assertFalse(cv)

    def test_valid(self):
        '''
        test validating a node through use 
        '''
        n = TestNode()
        n.valid()
        n.color='red'
        c = Condition(n, 'color', 'blue')
        self.assertFalse(c.valid())
        # false
        n.color = 'blue'
        self.assertTrue(c.valid())


def main():
    unittest.main()


if __name__ == '__main__':
    main()
