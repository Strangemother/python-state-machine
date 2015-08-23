import unittest
from mock import Mock, MagicMock
from ..node import Node
from ..machine.managers import Manager, ConditionsManager
from ..conditions import Condition
from ..machine import Machine, NodeManager

class ManagerTests(unittest.TestCase):

    def setUp(self):
        '''
        ManagerTests create manager
        '''
        self.m = Manager()

    def test_contains(self):
        '''
        An item can be appended though the machine
        '''
        n = 'foo'
        self.m.append(n)
        self.assertTrue(n in self.m)
        self.assertIn(n,self.m)

    def test_getitem(self):
        '''
        An item can be collected through __getitem__
        '''
        n = 'foo'
        self.m.append(n)
        d = self.m[n]
        self.assertIn(n, d)

    def test_get(self):
        '''
        An item can be collected through get()
        '''
        n = 'foo'
        self.m.append(n)
        d = self.m.get(n)
        self.assertIn(n, d)

    def test_append_calls_integrate_item(self):
        '''
        append calls integrate_item
        '''
        n = 'foo'
        m = Manager()
        m.integrate_item = MagicMock(return_value=n)
        m._names[n] = []
        m.append(n)
        m.integrate_item.assert_called_with(n)


    def test_append_calls_integrate_item_with_names(self):
        '''
        append calls integrate_item
        '''
        n = 'foo'
        names = ('bar', 'wibble',)
        m = Manager()
        m.integrate_item = MagicMock(return_value=n)
        m._names[n] = []
        m.append_with_names(names, n)
        m.integrate_item.assert_called_with(n, names)

class ConditionManagerTests(unittest.TestCase):

    def test_get_item_names(self):
        c = Condition('foo', 'bar', 1)

        cm = ConditionsManager()

        tpl = cm.get_item_names(c)

        self.assertIn('foo', tpl)


class NodeManagerTests(unittest.TestCase):

    def setUp(self):
        self.m = NodeManager()

    def test_can_append(self):
        '''
        A node can be appended though the machine
        '''
        n = Node()
        n.name = 'foo'
        self.m.append(n)
        self.assertIn(n, self.m)

    def test_get_by_name(self):
        '''
        an appened node can be found through get()
        '''
        n = Node()
        n.name = 'foo'
        self.m.append(n)
        r = self.m.get(n.get_name())
        self.assertIn(n, r)
