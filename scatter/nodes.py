'''
A Node is the endpoint to the API, exposed to integrate into your
logic. Defining a class extending Node class provides a dispatch routine
when integrated to a Machine.
The Machine monitors a Node - or more precisely, monitors Node._event
with a callback.
A node is a very simple object designed to be lightweight for maximum
pliability. The Machine handles the heavy load.
'''
from conditions import ConditionsMixin
from mixins import GetSetMixin, NameMixin, EventMixin
from managers import NodeManager


class Node(NameMixin, ConditionsMixin, GetSetMixin, EventMixin):
    '''
    A node is simply an object of which dispatches it's value changes through
    a single member. By inheriting the GetSetMixin all none existent attributes
    are perpetuated through `get`. All applied changes to keys are pass through
    `set`
    If __getattr__ key is defined the local value is provided.
    '''

    def __init__(self, name=None):
        '''
        The init method has very little to do (hopefully less)
        the self._event_handlers is instantiated for Machine callback.
        This should be taken off the __init__ eventually.
        '''
        self._build_event()
        self._name = name

    def set(self, k, v):
        self._dispatch('set', k, v)
        super(Node, self).set(k, v)


class NodeMixin(object):
    '''
    Mixin to assist in managing and reading Nodes in a Manager list.
    '''
    nodes = None

    def _setup_nodes(self, node_callback=None):
        self._node_callback = node_callback or self.node_event_handler
        self.nodes = NodeManager(self._add_node_event_handler)

    def _add_node_event_handler(self, node):
        '''
        Callback for a node being added to the node manager.
        '''
        # provide the node handler to the node
        print 'node %s has been added to nodes' % (node, )
        node._event_handlers += self._node_callback

    def node_event_handler(self, node, *args, **kw):
        '''
        This method is provided to NodeManager manager upon instansiation
        and is called through the event library.
        '''
        import pdb; pdb.set_trace()  # breakpoint c0622778 //
        print 'NodeMixin::node_event_handler::', node, args, kw
