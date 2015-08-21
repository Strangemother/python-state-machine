from axel import Event
from managers import NodeManager, ConditionsManager
from pprint import pprint


class NodeMixin(object):
    '''
    A set of tools to call lazy objects from the network within the machine.
    '''
    nodes = NodeManager()

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

        # print 'dispatch ask'
        # print 'receive ask'
        # print 'provide lazy object to callback'

        return nodes

class Connection(object):

    def connect(self):
        print 'perform connection'

        # Does this connection exist?
        #   Join
        # else Create and join


class Conditions(object):


    def read_conditions(self, node):
        '''
        Read the conditions of a node.
        '''
        cnds = node.conditions()
        print 'get conditions for node', node
        for c in cnds:
            self.integrate_condition(c, node)

    def integrate_condition(self, cond, node):
        names = self.get_integration_names(node, cond)
        print 'integrate conditions', node, cond, names
        self.conditions.append_with_names(names, cond)
        # node, condition assications
        ck = self.condition_keys
        sc = str(cond)

        if (sc in ck) is False:
            ck[sc] = []

        ck[sc].append(node.get_name())


    def get_integration_names(self, node, condition):
        node_name = node.get_name()
        names = (node_name, str(condition), )
        return names

    def _integrate_condition(self, condition, node):
        '''
        integrate the condition into the chain, calling
        the node when the condition is met.
        '''
        # print '+   integrate_condition', condition
        ks = self.condition_keys
        c = condition

        ng_name = node.get_name()
        node_name = c.watch
        # name used in keys and flat
        name = '{0}-{1}' .format(ng_name, str(c) )
        # by sub string {watch}_{field}
        ss = '{0}-{1}_{2}'.format(ng_name, node_name, c.field)
        condition_name = '{0}_{1}'.format(node_name, c.field)
        condition_full = '{0}_{1}_{2}'.format(node_name, c.field, c.target)

        cnodes = self.condition_nodes

        # by node name.
        if (node_name in ks) is False:
            # add list for conditions by name
            ks[node_name] = []

        if (ss in ks) is False:
            ks[ss] = []

        if (name in ks) is False:
            ks[name] = []

        if (ng_name in cnodes) is False:
            cnodes[ng_name] = []

        if (name in cnodes) is False:
            cnodes[name] = []


        if (condition_name in ks) is False:
            ks[condition_name] = []

        if (condition_full in ks) is False:
            ks[condition_full] = []

        if (condition_name in cnodes) is False:
            cnodes[condition_name] = []


        # Flat lit of all conditions, met with string weakref
        cnds = self.conditions

        # add to flat table.
        cnds[name] = condition
        # add to many keys.
        ks[name].append(name)
        ks[node_name].append(name)
        ks[ss].append(name)
        ks[condition_name].append(name)
        ks[condition_full].append(name)
        cnodes[ng_name].append(name)
        cnodes[name].append(node)
        cnodes[condition_name].append(node)
        # print '+ ', name, '  Condition integrated'

    def run_conditions(self, conditions, node, value, field):
        # pprint(self.conditions._names)
        print 'run conditions', conditions, node, field
        pairs = []
        # fetch associated conditions.
        # print 'nodes on name', node.get_name(), self.conditions.get( node.get_name() )
        # make the condition perform the compare
        for cond in conditions:
            # print 'looking at', cond
            print self.condition_keys
            # get associated nodes for the condition
            node_names = self.condition_keys.get(str(cond)) or []
            # loop and get associated condition
            for nn in node_names:
                s = '{0}-{1}'.format(nn, str(cond))
                r= self.conditions.get(s) or []
                # print 'looking for', s, r
                pairs.extend( [(self.nodes.get(nn), r,)] )

        res = {}
        for parent_nodes, _conditions in pairs:
            for cnd in _conditions:
                for pn in parent_nodes:
                    v = cnd.validate(pn, node, value, field)
                    print '  ', cnd, '==', v
                    n = '{0}-{1}'.format(pn.get_name(), str(cnd))
                    res[n]= v

        print 'Found ', res

        return res

        for condition in set(_conditions):
            # get matching conditions for names.
            print parent_node_name, node, field
            n = '{0}-{1}_{2}'.format(parent_node_name, node.get_name(), field)
            print 'parent_conditions ', n
            parent_conditions = self.conditions.get(n) or []
            print 'parent_conditions', parent_conditions
            conds += [ (parent_node_name, x,) for x in parent_conditions]
        print 'conditions match', conds

        for pn, cnd in conds:
            # print '  condition', cnd, cnd.target, 'for', pn
            v = cnd.validate(pn, node, value, field)
            # print '  ', cnd, '==', v

    def find_conditions(self, node, field, value):
        print 'find conditions for', node, field, value
        n = '{0}_{1}_{2}'.format(node.get_name(), field, value)
        # print '+  find conditions on', n
        cnds = self.get_conditions(node, field, value)
        print '-- Matches condition', cnds
        return cnds

    def get_conditions(self, node, name, value=None):
        '''
        Get conditions based upon node and name
        '''
        node_name = node
        print 'get condition', node, name, value
        cnds = self.conditions

        if hasattr(node_name, 'get_name'):
            node_name = node.get_name()
        name1 = '{0}_{1}'.format(node_name, name)

        match_names = (name1, )

        # exact match string
        if value is not None:
            vcn = '{0}_{1}_{2}'.format(node_name, name, value)
            match_names += (vcn,)

        print '  try: ', match_names

        res = []
        for _n in match_names:
            res += self.get_conditions_by_name(_n) or []
        print 'found conditions', res
        return set(res)

    def get_conditions_by_name(self, name):
        '''
        return the conditions matching a name provided.
        '''
        cnds = self.conditions.get(name)

        # print 'get_condition_by_name:', name, cnds
        return cnds

    def condition_name(self, node, name, *args, **kw):
        '''
        create a name for a condition string match from the
        values passed.
        The node is the original object receiving the change.
        name denoted the key changing.
        returned is a string for the condition
        '''
        n = node.get_name()
        a = [n, args[0]]
        s = '_'.join(a)
        return s


class EventsAPI(object):

    def on_event(self, name, node, *args, **kw):
        pass
        # print 'EVENT', name, node


class Events(EventsAPI):

    def node_event(self, node, name, *args, **kw):
        # print '-- Event:', str(node), name, args, kw
        # s = self.condition_name(node, name, *args, **kw)

        if name == 'set':
            self.event_set(node, *args, **kw)
        self._dispatch(name, node, *args, **kw)
        # The value has been set.
        # check the condition of other nodes.

    def event_set(self, node, *args, **kw):
        '''
        the set event passing the node field and value.
        optional original value for direction calculation
        '''
        field = args[0]
        v = args[1]

        cnds = self.find_conditions(node, field, v)
        return self.run_conditions(cnds, node, v, field)

    def _dispatch(self, name, node, *args, **kw):
        '''
        Dispatch en event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        self.on_event(name, node, *args, **kw)
        # print 'dispatch', name, args[0]
        if self._event is not None:
            res = self._event(name, node, *args, **kw)

            if res is not None:
                self.event_result(res)
        else:
            print 'x  ', self, "Error on _event existence"

    def dispatch_integrate(self, node):
        return self._dispatch('integrate', node)

    def dispatch_init(self, name):
        return self._dispatch('init', name)

    def event_result(self, flag, result, handler):
        if flag is False:
            raise result


class Nodes(Events):

    def add(self, *args):
        '''
        add a node to the manager
        '''
        for node in args:
            # print '+   add_node', node
            self.nodes.append(node)
            self.integrate_node(node)

    def integrate_node(self, node):
        self.read_conditions(node)
        node._event += self.node_event
        self.dispatch_integrate(node)
        node.react = True

class Machine(Connection, Nodes, Conditions, NodeMixin):
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
       self.dispatch_init(name)

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

    def loop(self):
        while self._stop == False:
            pass
