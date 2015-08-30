import unittest
from mock import Mock
from ..machine import Machine
from ..node import Node
from machine.address import Address

class AddressTest(unittest.TestCase):

    def setUp(self):
        self.m = Machine('foo')
        self.n = Node('TestNode')

    def test_make_machine_address(self):
        '''
        An address item has a make function
        '''
        self.assertTrue( hasattr(a, '_make'))

    def test_make_machine_address(self):
        '''
        make an address based on machine
        '''

        m2 = Machine('bar')
        m3 = Machine('baz')

        a = Address()._make(machine=self.m)
        self.assertEqual(str(a), 'machine.foo')

        a = Address()._make(machines=[self.m])
        self.assertEqual(str(a), 'machine.foo')

        a = Address()._make(machines=[self.m, m2])
        self.assertEqual(str(a), 'machine.foo+bar')

        a = Address()._make(machine=self.m, machines=[m2, m3])
        self.assertEqual(str(a), 'machine.foo+bar+baz')

    def test_make_node_address(self):
        '''
        _make method with nodes
        '''
        n2 = Node('FooNode')
        n3 = Node('GabeNode')

        a = Address()._make(node=self.n)
        self.assertEqual(str(a), 'node.TestNode')

        a = Address()._make(nodes=[self.n])
        self.assertEqual(str(a), 'node.TestNode')

        a = Address()._make(nodes=[self.n, n2])
        self.assertEqual(str(a), 'node.TestNode+FooNode')

        a = Address()._make(node=self.n, nodes=[n2, n3])
        self.assertEqual(str(a), 'node.FooNode+GabeNode+TestNode')

    def test_make_machine_node_address(self):
        '''
        Node on machine specific message
        '''

        m2 = Machine('bar')
        m3 = Machine('baz')

        n2 = Node('FooNode')
        n3 = Node('GabeNode')

        # machine and node
        a = Address()._make(machine=m2, node=n2)
        self.assertEqual(str(a), 'node.bar.FooNode')

        # machines and node
        a = Address()._make(machines=[m2,m3], node=n2)
        self.assertEqual(str(a), 'node.bar+baz.FooNode')

        # machine and nodes
        a = Address()._make(machine=m2, nodes=[n2, n3])
        self.assertEqual(str(a), 'node.bar.FooNode+GabeNode')

        # machines and nodes
        a = Address()._make(machines=[m2,m3], nodes=[n2, n3])
        self.assertEqual(str(a), 'node.bar+baz.FooNode+GabeNode')

        # machine, machines, node and nodes
        a = Address()._make(machine=self.m, machines=[m2,m3], nodes=[n2, n3])
        self.assertEqual(str(a), 'node.foo+bar+baz.FooNode+GabeNode')

        # node.foo+bar+baz.FooNode+GabeNode+TestNode
        kw = {  'machine': self.m,
                'machines': [m2,m3],
                'node': self.n,
                'nodes': [n2, n3],
            }

        a = Address()._make(**kw)
        self.assertEqual(str(a), 'node.foo+bar+baz.FooNode+GabeNode+TestNode')

    def test_change_seperator(self):
        '''
        Alter string mapping seperator
        '''
        m2 = Machine('bar')
        m3 = Machine('baz')

        n2 = Node('FooNode')
        n3 = Node('GabeNode')

        # machine and node
        a = Address()
        a.seperator = ':'
        a._make(machine=m2, node=n2)
        self.assertEqual(str(a), 'node:bar:FooNode')

        a.seperator = '>'
        self.assertEqual(str(a), 'node>bar>FooNode')

        a.seperator = None
        self.assertEqual(str(a), 'nodebarFooNode')

        a.seperator = Address.SEP
        self.assertEqual(str(a), 'node.bar.FooNode')

    def tool_items(self):
        '''
        Alter string mapping seperator
        '''
        m2 = Machine('bar')
        m3 = Machine('baz')

        n2 = Node('FooNode')
        n3 = Node('GabeNode')

        return (m2, m3, n2,n3)

    def test_node_string_prefix(self):
        '''
        A node only name will be prefixed through
        address.
        '''
        # machine and node
        a = Address('TestNode')
        self.assertEqual(str(a), 'node.TestNode')

    def test_node_node_spelling(self):
        '''
        An address can handle a node called 'node'
        '''
        a = Address('node.node')
        self.assertEqual(str(a), 'node.node')

        a = Address('node')
        self.assertEqual(str(a), 'node.node')

    def test_node_prefixed_prior(self):
        '''
        An address will not re-prefix an address
        '''
        a = Address('node.TestNode')
        self.assertEqual(str(a), 'node.TestNode')

    def test_node_name_nodes_list(self):
        '''
        An address can accept a name and a list of nodes.
        Named node is last.
        '''
        m2,m3,n2,n3 = self.tool_items()
        a = Address('TestNode', nodes=[n2])
        self.assertEqual(str(a), 'node.FooNode+TestNode')

        # Can be done with prefix
        a = Address('node.TestNode', nodes=[n2])
        self.assertEqual(str(a), 'node.FooNode+TestNode')

    def test_node_name_nodes_list_node(self):
        '''
        Address can handle name, node and nodes list
        Named is last.
        '''
        m2,m3,n2,n3 = self.tool_items()
        a = Address('TestNode', nodes=[n2], machines=[m2])
        self.assertEqual(str(a), 'node.bar.FooNode+TestNode')

        # same with prefix
        a = Address('node.TestNode', node=n3, nodes=[n2])
        self.assertEqual(str(a), 'node.FooNode+TestNode+GabeNode')

    def test_node_name_list_with_machine(self):
        '''
        An address can accept a name, nodes, machine and machine.
        named node is last.
        '''
        m2,m3,n2,n3 = self.tool_items()
        a = Address('TestNode', nodes=[n2], machine='baz', machines=[m2])
        self.assertEqual(str(a), 'node.baz+bar.FooNode+TestNode')
