import unittest
from scatter.adapters import BaseAdapter, PyroAdapter
from mock import MagicMock, call


class MockBridge(object):
    wibble = 'dibble'

    def call(self, key):
        pass


class MockMachine(object):

    def node_set_event(self, key, current, incoming, node):
        pass


class TestBaseAdapter(unittest.TestCase):
    '''
    Tests for a BaseAdapter
    '''

    def test___getattr__(self):
        '''
        getattr from an adapter will pass-through to the bridge.
        '''
        name = 'base'
        base_adapter = BaseAdapter(name, bridge=MockBridge())
        self.assertEqual('dibble', base_adapter.__getattr__('wibble'))

    def test___getitem__(self):
        name = 'base'
        base_adapter = BaseAdapter(name, bridge=MockBridge())
        self.assertEqual('dibble', base_adapter.__getitem__('wibble'))

    def test___init___name_only(self):
        '''
        ___init___ can receive name only,
        '''
        name = 'dave'
        base_adapter = BaseAdapter(name)
        self.assertEqual(base_adapter.name, name)
        # Bridge should exist
        self.assertIsNotNone(base_adapter.bridge)

    def test___init___item(self):
        '''
        ___init___ can receive name only and item
        '''
        name = 'dave'
        item = {}
        base_adapter = BaseAdapter(name, item)
        self.assertEqual(base_adapter.name, name)
        # keeps reference of item
        self.assertEqual(base_adapter.item, item)
        # Bridge should exist
        self.assertIsNotNone(base_adapter.bridge)

    def test___init___bridge(self):
        '''
        ___init___ can accept an instance of a bridge
        '''
        name = 'dave'
        base_adapter = BaseAdapter(name, bridge=MockBridge())
        self.assertIsInstance(base_adapter.bridge, MockBridge)

    def test_add(self):
        '''
        Add a peer to the connection pool
        '''
        base_adapter = BaseAdapter('base')
        name='foo'
        uri ='some string'
        # returns name
        self.assertEqual(name, base_adapter.add(name, uri))
        self.assertIn(name, base_adapter.connections)

    def test_call_item(self):
        kw = {
            'node': 'nodeName',
            'machine': 'myMachine',
        }
        args = ('key', 1, 2)
        event = 'set'
        name ='base'
        item = MockMachine()
        item.node_set_event = MagicMock()

        base_adapter = BaseAdapter(name, item)
        base_adapter.call_item(event, *args, **kw)
        item.node_set_event.assert_called_with(*args, node=kw['node'])

    def test_get_object(self):
        base_adapter = BaseAdapter('name')
        uri = 'some connection string'
        self.assertEqual(uri, base_adapter.get_object(uri))

    def test_node_event(self):
        kw = {
            'node': 'nodeName',
            'machine': 'myMachine',
        }
        args = ('key', 1, 2)
        event = 'set'
        name ='base'
        item = MockMachine()
        item.node_set_event = MagicMock()

        base_adapter = BaseAdapter(name, item)
        base_adapter.call_item = MagicMock()
        base_adapter.send_to = MagicMock()

        base_adapter.connections = {
            'foo': 1,
            'myMachine': 'skipped',
        }

        base_adapter.node_event(event, *args, **kw)
        # pass through
        base_adapter.call_item.assert_called_with(event, *args, **kw)
        # skips myMachine
        base_adapter.send_to.assert_called_once_with('foo', 'node_event', event, *args, **kw)

    def test_send(self):
        name ='base'
        item = MockMachine()
        base_adapter = BaseAdapter(name, item)
        base_adapter.send_to = MagicMock()

        args = ('key', 1, 2)
        kw = {
            'node': 'nodeName',
            'machine': 'myMachine',
        }

        calls = [
            call('foo', 'key', *args, **kw),
            call('myMachine', 'key', *args, **kw),
        ]

        base_adapter.connections = {
            'foo': 1,
            'myMachine': 'skipped',
        }

        base_adapter.send('key', *args, **kw)
        base_adapter.send_to.assert_has_calls(calls, any_order=True)

    def test_send_return(self):
        name ='base'
        base_adapter = BaseAdapter(name)

        def se(name, key, *args, **kw):
            return name

        base_adapter.send_to = MagicMock(side_effect=se)

        args = ('key', 1, 2)
        kw = {}

        base_adapter.connections = {
            'foo': 1,
            'myMachine': 'skipped',
        }

        res = base_adapter.send('key', *args, **kw)
        self.assertDictEqual(res, {
                'foo': 'foo',
                'myMachine': 'myMachine',
            })

    def test_send_to(self):
        base_adapter = BaseAdapter('name')
        b = MockBridge()
        b.call = MagicMock(return_value='bridge_result')
        base_adapter.get_object = MagicMock(return_value=b)
        base_adapter.connections = {
            'foo': 'connection string',
        }
        args = (1, 2,)
        kw = {
            'node': 'nodeName',
            'machine': 'myMachine',
        }

        b_res = base_adapter.send_to('foo', 'key', *args, **kw)
        # The return should be from the bridge call.
        self.assertEqual(b_res, 'bridge_result')
        # Connection object should have been fetched
        base_adapter.get_object.assert_called_with('connection string')
        # bridge.call() should have been called
        b.call.assert_called_with('key', *args, **kw)


class TestPyroAdapter(unittest.TestCase):
    def test___init__(self):
        name = 'adap'
        item = {}
        bridge = MockBridge()
        pyro_adapter = PyroAdapter(name, item, bridge)
        self.assertEqual(pyro_adapter.bridge, bridge)
        self.assertEqual(pyro_adapter.name, name)
        self.assertEqual(pyro_adapter.item, item)

    def test_daemon(self):
        '''
        calling daemon() will create a self._daemon instance
        '''
        pyro_adapter = PyroAdapter('name')
        # created instance
        d = pyro_adapter.daemon()
        self.assertEqual(pyro_adapter._daemon, d)

    def test_daemon_setup(self):
        '''
        calling daemon() will create a self._daemon instance
        '''
        pyro_adapter = PyroAdapter('name')
        pyro_adapter.setup = MagicMock()
        # created instance
        pyro_adapter.setup.asset_called()

    def test_daemon_exists(self):
        '''
        an existing daemon is reused and returned.
        '''
        mock_daemon = {}
        pyro_adapter = PyroAdapter('name')
        pyro_adapter._daemon = mock_daemon
        # created instance
        self.assertEqual(pyro_adapter.daemon(), mock_daemon)

    def test_daemon_pyro_instance(self):
        '''
        an existing daemon is reused and returned.
        '''
        from Pyro4 import Daemon

        pyro_adapter = PyroAdapter('name')
        # created instance
        self.assertIsInstance(pyro_adapter.daemon(), Daemon)

    def test_generate(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.generate(bridge))
        assert False # TODO: implement your test here

    def test_get_nameserver(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.get_nameserver())
        assert False # TODO: implement your test here

    def test_get_object(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.get_object(uri))
        assert False # TODO: implement your test here

    def test_get_uri(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.get_uri(bridge))
        assert False # TODO: implement your test here

    def test_register(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.register(item))
        assert False # TODO: implement your test here

    def test_setup(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.setup())
        assert False # TODO: implement your test here

    def test_wait(self):
        # pyro_adapter = PyroAdapter(name, item, bridge)
        # self.assertEqual(expected, pyro_adapter.wait(bridge))
        assert False # TODO: implement your test here


if __name__ == '__main__':
    unittest.main()
