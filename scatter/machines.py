from axel import Event

from nodes import NodeMixin
from managers import NodeManager, ConditionsManager
from time import time as _time
from mixins import EventMixin


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
        Returns a string version of the node
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
        '''
        # hooking from ManagerMachine._add_node_event
        print 'machine heard node change', str(node), args

        self.node_event(args[0], node, *args, **kw)


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
        import pdb; pdb.set_trace()  # breakpoint fcbf1cc3 //

        self.conditions.integrate_conditions(conditions, node)


class Machine(MachineBase, EventCoupler, NodeMixin, EventMixin):

    def setup(self):
        '''
        Setup the node manager calling the super once complete.
        '''
        print '>       setup Conditions'
        self.conditions = ConditionsManager()
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
        print 'machine heard add node event', node
        cnds = self._read_conditions(node)
        print 'conditions', cnds
        self._add_conditions(cnds, node)
        return super(Machine, self)._add_node_event_handler(node)

    def node_event(self, name, node, *args, **kw):
        '''
        This method is provided to NodeManager manager upon instansiation
        and is called through the event library.
        '''
        print 'Machine::node_event::', name, type(node), str(node)
