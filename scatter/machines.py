from axel import Event
from managers import NodeManager, BridgeManager
from mixins import ManagerMixin
from bridge import BridgeMixin
from adapters import PyroAdapter, AdapterMixin


class MachineBase(object):

    def send(self, event, *args, **kw):
        '''
        Send the value through the adapter
        '''
        self.adapter.send(event, *args, **kw)

    def __str__(self):
        ''' Returns a string version of the machine '''
        return '{0}({1})'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return '<machine.Machine:{0}>'.format(self.__str__())


class Machine(MachineBase, ManagerMixin, BridgeMixin, AdapterMixin):
    ''' The machine connects the nodes and manages the addition
    and removal of nodes to the network. '''

    def __init__(self, name=None, bridge=None):
        '''sets the name and calls the setup() method'''
        if name is not None:
            self.name = name
        self.setup()
        self.bridge = self.make_bridge()
        self.adapter = self.make_adapter(self.name, self.bridge)

    def wait(self):
        self.adapter.wait()

    def setup(self):
        ''' Setup the node manager calling the super once complete.
        Add event tool and store the time of call as unix'''
        # ManagerMixin
        self.nodes = self.make_manager(NodeManager, self._node_event)
        self.peers = self.make_bridge_manager(BridgeManager)
        self._event = Event(self)

    def _node_event(self, node, *args, **kw):
        ''' Callback for a node being added to the node manager.

        When the NodeManager was instantiated, this method was provided as
        the callback to respond to an event dispatched from a node. '''
        # machine, node, *events, anything else.
        self.node_event(self, node, *args, **kw)

    def node_event(self, machine, node, event, *args, **kw):
        ''' This method is provided to NodeManager manager upon instansiation
        and is called through the event library. '''
        if event == 'set':
            # A name args tuple will have (event, key, value)
            key = args[0]
            print 'args', machine, node, args, kw
            current = node.get(key)
            incoming = args[1]
            # Reacting to a set is the only hardwired functionality.
            self.node_set_event(key, current, incoming, node)

        kw = {
            'node': node.get_name(),
            'machine': self.name,
        }

        self.send('node_event', event, key, current, incoming, **kw)

        for bridge in self.peers:
            print 'bridge', bridge
            print event, key, current, incoming
            bridge.call('node_event', event, key, current, incoming, **kw)

    def node_set_event(self, key, current, incoming, node=None, machine=None):
        ''' this method called by self.node_event iterates the set event to the
        attached nodes.
        key is the attr on the node in the event context
        current is the existing value for the node attr
        incoming is the new value to be assigned to the node attr
        node is the event node in context. '''
        # Don't run the existing node,

        for n in self.nodes:
            if n is not node:# and node.get_name() == _node.get_name():
                n._run_conditions(key, current, incoming, node=node, machine=machine)
