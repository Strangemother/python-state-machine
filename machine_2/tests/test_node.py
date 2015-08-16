import unittest
from ..core.node import Node


class TestNode(Node):
    """TestNode"""

    foo = 'bar'
    bar = 2

    def __init__(self):
        super(TestNode, self).__init__()
    

class BasicTests(unittest.TestCase):

    def setUp(self):
       self.n = TestNode()
        
    def test_get_attrs(self):
        '''
        get the extended attributes from the Ndoe
        '''
        attrs = self.n.get_attrs()
        exp = ['foo', 'bar']
        self.assertItemsEqual(attrs, exp)

    def test_can_set(self):
        '''
        can set a value on a Node using the provided set method        
        '''
        old = self.n.foo
        self.n.set('foo', 'wibble')
        self.assertEqual(self.n.foo, 'wibble')

    def test_can_get(self):
        '''
        can get an attribute using the provided method
        '''
        v = self.n.foo
        self.assertEqual(self.n.get('foo'), v)

    def test_conditions(self):
        '''
        A Node returns a list of conditions to meet.
        '''
        cs = self.n.conditions()
        valid_types = (list, tuple,)
        self.assertTrue( isinstance(cs, valid_types) )


def main():
    unittest.main()


if __name__ == '__main__':
    main()