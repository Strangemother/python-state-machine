import unittest
from ..core import Node, Condition
from ..core.compares.simple import Exact
from ..core.compares.base import Compare 
from ..core.compares.const import *


# class TestCompare(unittest.TestCase):

#     def test_store_bad_key(self):
#         '''
#         attempting to store a key of which
#         does not exist will return false
#         '''
#         c = Condition(self.n, 'foo')
#         v = c.store('bad_key')
#         self.assertFalse(v)

#     def test_store_create_cache(self):
#         ''' A cache is automatically created when
#         required. The callbacks facilitate communication
#         '''
#         c = Condition(self.n, 'foo')
#         # cache should not exist
#         self.assertFalse( hasattr(c, '__cache') )
#         # cache data
#         c.store()
#         # cache should exist
#         self.assertTrue( hasattr(c, '__cache') )
        
#         expected = {
#             'foo': ['bar']
#         }

#         self.assertDictContainsSubset(c._get_cache(), expected)

#         d = Condition(self.n, 'foo')
#         # should not exist
#         self.assertFalse( hasattr(d, '__cache') )
#         # get cache
#         gc = d._get_cache()
#         # cache made
#         self.assertTrue( hasattr(d, '__cache') )
#         self.assertDictContainsSubset(gc, {})


#     def test_store_state(self):
#         # Value for 'bar'
#         val = 3
#         field = 'bar'
#         foo_field = 'foo'
#         foo_value = 'bar'

#         c = Condition(self.n, field)
#         self.n[field] = val

#         # no args
#         blank_store = c.store()

#         # a store without args implements the cache of bar
#         self.assertTrue(blank_store)
#         # can retrieve from cache call
#         self.assertEqual(c.store_cache(field), val)
        
#         # just keys
#         field_store = c.store(field)

#         # did store
#         self.assertTrue(field_store)
#         self.assertEqual(c.store_cache(field), val)

#         self.n[foo_field] = foo_value
#         # Use the cache on another key
#         c.store(foo_field)

#         # the previous key should persist.
#         self.assertEqual(c.store_cache(field), val)
#         # second cache persists
#         self.assertEqual(c.store_cache(foo_field), foo_value)

#     def test_store_manual_change(self):
#         # when bar on node == 4
#         self.n.bar = 2
#         c = Condition(self.n, 'bar', 4)
#         s = c.store()
#         self.assertTrue(s)

#         cv = c.store_cache('bar')
#         self.assertEqual(cv, self.n.bar)

#         self.n.bar = 3
#         s = c.store()
#         self.assertTrue(s)

#         cv = c.store_cache('bar')
#         self.assertEqual(cv, self.n.bar)


#         self.assertEqual(c._get_cache()['bar'], [2,3])

