from axel import Event
from managers import NodeManager
from mixins import ManagerMixin


class Machine(ManagerMixin):
    ''' The machine connects the nodes and manages the addition
    and removal of nodes to the network. '''

    def __init__(self, name=None):
        '''sets the name and calls the setup() method'''
        self.name = name
        self.setup()

    def setup(self):
        ''' Setup the node manager calling the super once complete.
        Add event tool and store the time of call as unix'''
        # ManagerMixin
        self.nodes = self.make_manager(NodeManager, self._node_event)
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
            current = node.get(key)
            incoming = args[1]
            # Reacting to a set is the only hardwired functionality.
            self.node_set_event(key, current, incoming, node)

    def node_set_event(self, key, current, incoming, node=None):
        ''' this method called by self.node_event iterates the set event to the
        attached nodes.
        key is the attr on the node in the event context
        current is the existing value for the node attr
        incoming is the new value to be assigned to the node attr
        node is the event node in context. '''
        # Don't run the existing node,
        for n in self.nodes:
            if n is not node:# and node.get_name() == _node.get_name():
                n._run_conditions(key, current, incoming, node)

    def __str__(self):
        ''' Returns a string version of the machine '''
        return '{0}({1})'.format(self.__class__.__name__, self.name)

    def __repr__(self):
        return '<machine.Machine:{0}>'.format(self.__str__())
