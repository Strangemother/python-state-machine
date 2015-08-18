import unittest
from mock import Mock
from ..runner import Runner, TestNode, TestReactNode
from ..machine import Machine
from ..node import Node

class NodeMixinTests(unittest.TestCase):

    def test_get_nodes(self):
        '''
        get_nodes returns list
        '''
        n = NodeMixin()
        self.assertIsInstance(n.get_nodes(), list)

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

        for c in cnds:
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
