import unittest
from core.machine import Register, Machine
from core.nodes import Nodes, Node
from core.events import Events


class T(Node):
    '''test node'''
    left = False
    right = False
    up = True
    down = False



class TestRun(unittest.TestCase):

    def setUp(self):
        self.machine = Machine('example')


    def test_register(self):
        pass

    def test_nodes(self):
        self.machine.render_nodes([T(),T(),T(),T()])
        assert len(self.machine.nodes) == 4

    def test_machine(self):
        # Machine can get a name
        m = Machine('test')
        self.assertEqual(m.name, 'test')
        m = Machine()

        self.assertGreater(len(m.name), len('test'))
        self.assertIsInstance(m.name, str)

        self.assertIsInstance(m.register, Register)
        self.assertIsInstance(m.events, Events)
        self.assertIsInstance(m.nodes, Nodes)

    def test_register(self):

        # Register needs machine
        def run_error_machine():
            r = Register()
            return r

        self.assertRaises(TypeError, run_error_machine)
        r = Register(self.machine)
        self.assertIsInstance(r, Register)


    def test_node_expose(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
