from axel import Event

from managers import NodeManager, ConditionsManager
from connection import Connection
from integration import ConditionIntegrate
from time import time as _time
from tools import color_print as cl
from bridge import Peers


class MachineBase(object):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    _stop = False
    peers = None
    remote = None

    def __init__(self, name=None):
        self.name = name
        self.setup(self.name)

    def setup(self, name=None):
        self._event = Event(self)
        self._start_time = int(_time())

    # def event_set(self, node, name, *args, **kw):
    #     # print '-- Machine Event:', str(node), '::', name, '::', args,'::', kw
    #     self.remote.set(node, name, args[0], args[1])
    #     super(Machine, self).event_set(node, name, *args, **kw)

    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.name,
        }

        return '<machine.Machine:{cls_name}("{name}")>'.format(**kw)



class MachineNodeIntegration(MachineBase):
    nodes = None

    def setup(self, name=None):
        '''
        Setup the node manager calling the super once complete.
        '''
        self.nodes = NodeManager(self._add_node_event)
        return super(MachineNodeIntegration, self).setup(name)

    def _add_node_event(self, node):
        '''
        Callback for a node being added to the node manager.
        '''
        node._event += self.node_event

    def node_event(self, name, node, *args, **kw):
        '''
        This method is provided to NodeManager manager upon instansiation
        and is called through the event library.
        '''
        print 'Machine::node_event::', name, type(node), str(node)


class MachineConditionIntegration(MachineBase):
    conditions = None

    def setup(self, name=None):
        self.conditions = ConditionsManager()
        return super(MachineConditionIntegration, self).setup(name)

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


class MachineRemoteIntegration(MachineBase):

    def setup(self, name=None):
        self.remote = Connection(self)
        self.dispatch_init(name)
        return super(MachineRemoteIntegration, self).setup(name)

    def dispatch_init(self, name, *args, **kw):
        return self._dispatch('init', name)

    def _dispatch(self, event_name, node, *args, **kw):
        '''
        Dispatch an event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        res = self.node_event(event_name, node, *args, **kw)

        if res is not None:
            self.event_result(res)
        return res


class MachinePeersIntegration(MachineBase):

    def setup(self, name=None):
        '''
        Create the peers for a machine to connect to.
        '''
        self.peers = Peers(self)
        super(MachinePeersIntegration, self).setup(name)


class Machine(MachineNodeIntegration, MachineConditionIntegration, \
              MachineRemoteIntegration, MachinePeersIntegration):

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

    def _add_node_event(self, node):
        '''
        Callback for a node being added to the node manager.
        '''
        # hooking from MachineNodeIntegration._add_node_event
        super(Machine, self)._add_node_event(node)
        cnds = self._read_conditions(node)
        self._add_conditions(cnds, node)
