from axel import Event

from managers import NodeManager, ConditionsManager
from time import time as _time
from mixins import EventMixin, NodeMixin


class MachineBase(object):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''

    def __init__(self, name=None):
        '''
        sets the name and calls the setup() method
        '''
        self.name = name
        self.setup()

    def setup(self):
        '''
        Add event tool and store the time of call as unix
        '''
        self._event = Event(self)
        self._start_time = int(_time())

    def __str__(self):
        '''
        Returns a string version of the machine
        '''
        return '%s "%s"' % (self.__class__.__name__, self.name, )

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.name,
        }

        return '<machine.Machine:{cls_name}("{name}")>'.format(**kw)


class EventCoupler(object):

    def _node_event(self, node, *args, **kw):
        '''
        Callback for a node being added to the node manager.

        When the NodeManager was instantiated, this method was provided as
        the callback to respond to an event dispatched from a node.
        '''
        # hooking from ManagerMachine._add_node_event
        # machine, node, *events, anything else.
        self.node_event(self, node, *args, **kw)

    def _read_conditions(self, node):
        '''
        Extract the conditions from a node returning conditions list
        '''
        cnds = tuple()
        if hasattr(node, 'conditions'):
            cnds = node.conditions()
        return cnds

    def _add_conditions(self, conditions, node):
        print 'add conditions', conditions, node
        self.conditions.integrate_conditions(conditions, node)


class Machine(MachineBase, EventCoupler, NodeMixin, EventMixin):

    def setup(self):
        '''
        Setup the node manager calling the super once complete.
        '''
        # self.conditions = ConditionsManager()
        self._setup_nodes(self._node_event)
        super(Machine, self).setup()

    def get_nodes(self, name=None):
        '''
        return a list of nodes for the associated name across the network.
        This can be a string or other valid reference.

        the fetch event is used to collect objects (or lazy objects)
        to the caller allowing for editing of nodes existing across the network
        '''
        if name is None:
            return self.nodes
        nodes = self.nodes.get(name)

        if nodes is None:
            # Get remote nodes.
            node_dict = self.remote.send('get_nodes', name)
            print 'remote nodes', node_dict
        return nodes

    def _add_node_event_handler(self, node):
        '''
        Callback for a node being added to the node manager.
        '''
        # cnds = self._read_conditions(node)
        #print 'conditions', cnds
        # self._add_conditions(cnds, node)
        return super(Machine, self)._add_node_event_handler(node)

    def node_event(self, machine, node, event, *args, **kw):
        # machine, node, *events, anything else.
        '''
        This method is provided to NodeManager manager upon instansiation
        and is called through the event library.
        '''
        # Iterate other nodes and check statements.
        if event == 'set':
            # A name args tuple will have (event, key, value)
            key = args[0]
            # Ecisting value
            current = node.get(key)
            if current is None:
                pass
                # print '--- Key %s is not accessible on %s' % (key, node)
            # new value.
            incoming = args[1]
            # print 'Machine::%s::%s::%s' % (node.get_name(), event, key)
            # Reacting to a set is the only hardwired functionality.
            self.node_set_event(key, current, incoming, node)

    def node_set_event(self, key, current, incoming, node=None):
        '''
        this method called by self.node_event iterates the set event to the
        attached nodes.
        key is the attr on the node in the event context
        current is the existing value for the node attr
        incoming is the new value to be assigned to the node attr
        node is the event node in context.
        '''
        for _node in self.nodes:
            # Don't run the existing node,
            # only run nodes of matching name
            if _node is not node: # and node.get_name() == _node.get_name():
                # print self, 'running conditions on', node, key, incoming
                _node._run_conditions(key, current, incoming, node)
