from base import Base
from nodes import Nodes, Node
from tools import random_string
from events import Events
import events
import inspect

class Register(Base):

    def __init__(self, machine, events=None):
        self.log_color = 'magenta'

        # Registeration of all named objects
        self.nodes = {}
        self.conditions = {}
        self.events = events
        self.machine = machine

    def event_handle(self, name, *args, **kwargs):
        self.log('REGISTER HEARD', name)
        self.iterate_conditions(name, **kwargs);

    def iterate_conditions(self, name, **kw):
        '''
        iterate the conditions for a given
        name.
        '''
        cnds = self.conditions.get(name, [])
        node = kw.get('node')

        for node_name in cnds:
            self.handle_condition(name, node_name, **kw)

    def handle_condition(self, cond, node_name, **kwargs):
        '''
        A condition is to be handled with the provided kwargs.
        This conditions reacts by collecting the live node from
        the machine network and calling a react.

        This method will be called by iterate_conditions many times
        based upon all condition names mateched in the conditions
        register.

        cond     a condition should be a Condition.get_name() value.
        node     the target node with the react() method to call.
        name     the name of the handling
        '''
        # get node,
        # handle condition
        ns = self.machine.nodes.get(node_name)
        for node in ns:
            # each node provided by get() from machine.
            node.met_condition(self.machine, cond)
            # valid = node.react(self.machine, condition=cnd)

    def add_node(self, node):
        n = node.get_name()

        if self.nodes.get(n) is None:
            # add to network.
            self.log('Register node', n)
            self.nodes[n] = {}
        self.add_conditions(node, node.get_conditions())

    def add_conditions(self, node, conditions):
        # loop conditions
        # add keys
        # dispatch events
        if conditions is None:
            return False

        for c in conditions:
            # get current conds object
            self.write_condition(node, c)

    def write_condition(self, node, condition):
        n = condition.get_name()
        cnds = self.conditions.get(n)

        if cnds is None:
            cnds = []
            self.events.listen(n, self.event_handle)

        # add reactive node to conditions
        cnds.append(node.get_name())
        self.conditions[n] = cnds
        self.log('write', node, condition)


class Machine(Base):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    def __init__(self, name=None):
        self.log_color = 'red'
        self.name = name or random_string(8)
        self.events = Events()
        events.e = self.events
        self.nodes = Nodes()
        self.register = Register(machine=self, events=self.events)

    def set_listeners(self):
        '''
        provide machine event listeners
        '''
        self.events.listen('add_conditions')


    def activate_node(self, node):
        _n = node.integrate(self)
        self.nodes.append(_n)
        self.log('Integrating node', _n)

        '''
        Loop an iterable to add Conditiond into the
        network for a node
        '''

        # Write node into register.
        # n=node.get_name()

        # add weak reference in register.
        self.register.add_node(_n)
        _n.react(self)
        return _n


    def render_nodes(self, nodes):
        self.log('Add nodes to network')

        for node in nodes:
            n = node
            # Create the node is the element is not an instance
            if inspect.isclass(node):
                n = node()
            self.activate_node(n)

    def start(self, nodes=None):
        if nodes is not None:
            self.render_nodes(nodes)
        print '\n--- Run ---\n'
        self.started(nodes)

    def started(self, nodes):
        '''
        Override for easy start reference. Passed are the initial
        nodes provides to the machine.
        '''
        pass


    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )
