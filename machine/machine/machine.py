from pprint import pprint

from axel import Event

from managers import NodeManager, ConditionsManager
from bridge import Connection
from integration import ConditionIntegrate, NodeIntegrate

from tools import color_print as cl


class Machine(NodeIntegrate, ConditionIntegrate):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    _stop = False

    def __init__(self, name=None):
       self.name = name
       self.conditions = ConditionsManager()
       self.condition_keys = {}
       self.condition_nodes = {}
       self.nodes = NodeManager(self.nodemanager_event)
       self._event = Event(self)
       cl('cyan', 'Ready Machine', name)
       self.dispatch_init(name)
       self.remote = Connection(self)

    def event_set(self, node, name, *args, **kw):
        # print '-- Machine Event:', str(node), '::', name, '::', args,'::', kw
        self.remote.set(node, name, args[0], args[1])
        super(Machine, self).event_set(node, name, *args, **kw)

    def get_nodes(self, name=None):
        '''
        return a list of nodes for the associated name across the network.
        This can be a string or other valid reference.

        the fetch event is used to collect objects (or lazy objects)
        to the caller allowing for editing of nodes existing across the network
        '''
        nodes = []
        # print 'get_nodes', name
        if name is None:
            return self.nodes

        if (name in self.nodes) is False:
            print 'node is not local'
        else:
            nodes = self.nodes[name]
            #print 'found nodes', nodes
        return nodes

    def nodemanager_event(self, name, node):
        print 'NodeManager event', name, node
        if name == 'integrate':
            self.integrate_node(node)

    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.name,
        }

        return '<machine.Machine:{cls_name}("{name}")>'.format(**kw)

    def add_peer(self, string):
        self.remote.peers.append(string)

    def online(self):
        self.remote.create()
        self.loop()

    def loop(self):
        self.remote.wait()
