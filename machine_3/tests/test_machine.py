import unittest
from mock import Mock

from ..machine import NodeMixin, Machine, NodeManager
from ..runner import Runner
from ..examples.basic import TestNode, TestReactNode
from ..node import Node

from ..machine.managers import ConditionsManager
from ..conditions import Condition



class ConditionsTest(unittest.TestCase):

    def test_condition_names(self):
        cds = ConditionsManager()
        c= Condition('foo', 'bar',3)
        cds.append_with_names( ('wibble', 'tos',), c)
        self.assertIn('wibble', cds._names)


class NodeMixinTests(unittest.TestCase):

    def test_get_nodes(self):
        '''
        get_nodes returns list
        '''
        n = NodeMixin()
        self.assertIsInstance(n.get_nodes(), NodeManager)



class NodeManagerTests(unittest.TestCase):

    def setUp(self):
        self.m = NodeManager()

    def test_can_append(self):
        n = Node()
        n.name = 'foo'
        self.m.append(n)
        self.assertIn(n, self.m)

    def test_get_by_name(self):
        n = Node()
        n.name = 'foo'
        self.m.append(n)
        r = self.m.get(n.get_name())
        self.assertIn(n, r)


class MachineTests(unittest.TestCase):

    def setUp(self):
       self.r = Runner()
       self.m = Machine('TestMachine')

    def test_make_machine(self):
        '''
        Machine should be instance of Machine
        '''
        self.assertTrue(isinstance( self.m, Machine ))

    def test_add(self):
        '''
        Can add a node to a machine
        '''
        n = Node()
        self.m.add(n)
        self.assertIn(n, self.m.nodes)
        self.assertTrue(n.react)

    def test_add_many(self):
        '''
        Can add a node to a machine
        '''
        n = Node()
        n2 = Node()
        self.m.add(n, n2)
        self.assertIn(n, self.m.nodes)
        self.assertIn(n2, self.m.nodes)
        self.assertTrue(n.react)
        self.assertTrue(n2.react)


    def test_integrate(self):
        '''
        Can integrate node with event listeners
        '''
        n = Node()
        ec = n._event.count()
        self.m.add(n)
        ec2 = n._event.count()
        # Count of active handlers from the machine.
        self.assertEqual(ec2 - ec, 1)
        # react should be turned on
        self.assertTrue(n.react)

    def test_integrate_conditions(self):
        '''
        Can collect conditions and integrate their strings.
        '''
        n = TestNode()
        self.m.add(n)
        cnds = n.conditions()
        keys = self.m.condition_keys
        # print 'keys', keys

        for c in cnds:
            # print 'c in',c
            self.assertTrue(str(c) in keys)

    def test_node_event(self):
        '''
        A change in node value dispatches an event through the machine
        '''
        n = TestNode()
        self.m.add(n)
        # a mock handler.
        f = Mock()
        # Add to the event handlers
        n._event += f
        # change for event reaction
        n.age = 4
        # Perform the action denoted.
        f.assert_called_with(n, 'set', 'age', 4, 22)

    def test_get_conditions(self):
        '''
        Can fetch conditions from the machine by name after
        a node has been added.
        '''
        n = TestReactNode()
        self.m.add(n)
        cnds = self.m.get_conditions('TestNode', 'age')
        # should find a condition or two.
        self.assertTrue(len(cnds) > 0)

    def test_get_condition_by_name(self):
        '''
        Can use get_conditions_by_name on machine to use
        a string to receive a list of conditions
        '''
        n = TestReactNode()
        self.m.add(n)
        cnds = self.m.get_conditions_by_name('TestNode_age')
        self.assertTrue(len(cnds) > 0)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
