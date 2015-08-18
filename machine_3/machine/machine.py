from axel import Event

class NodeMixin(object):
    '''
    A set of tools to call lazy objects from the network within the machine.
    '''
    nodes = None

    def get_nodes(self, name):
        '''
        return a list of nodes for the associated name across the network.
        This can be a string or other valid reference.

        the fetch event is used to collect objects (or lazy objects)
        to the caller allowing for editing of nodes existing across the network
        '''
        nodes = []
        print 'get_nodes', name
        if (name in self.node_names) is False:
            print 'node is not local'
        else:
            nodes = self.node_names[name]
            print 'found nodes', nodes

        print 'dispatch ask'
        print 'receive ask'
        print 'provide lazy object to callback'

        return nodes

class Machine(NodeMixin):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    def __init__(self, name=None):
       self.name = name
       self.conditions = {}
       self.condition_keys = {}
       self.condition_nodes = {}

       self.nodes = []
       self.node_names = {}
       self._event = Event(self)

    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )

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
        node.react = True
        n = node.get_name()
        if (n in self.node_names) is False:
            self.node_names[n] = []

        self.node_names[n].append(node)

        print '++  Machine: node', node, 'integrated'

    def read_conditions(self, node):
        '''
        Read the conditions of a node.
        '''
        cnds = node.conditions()

        for c in cnds:
            self.integrate_condition(c, node)

    def integrate_condition(self, condition, node):
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
        cnodes[ng_name].append(name)
        cnodes[name].append(node)
        cnodes[condition_name].append(node)
        print '+ ', name, '  Condition integrated'

    def node_event(self, node, name, *args, **kw):
        print '-- Event:', str(node), name, args, kw
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
        n = '{0}_{1}_{2}'.format(node.get_name(), field, v)
        print '+  find conditions on', n
        cnds = self.get_conditions(node, field, v)
        print '-- Matches condition', cnds
        self.run_conditions(cnds, node, v, field)

    def run_conditions(self, conditions, node, value, field):
        # print 'run conditions', conditions
        n = '{0}_{1}'.format(node.get_name(), field)
        print '! Conditions for ', n
        parent_nodes = self.condition_nodes.get(n)
        # make the condition perform the compare
        conds = []
        _ = self.conditions.get

        if parent_nodes is None:
            print '!  no parent nodes for', n
            return None

        for pn in set(parent_nodes):
            # get matching conditions for names.
            n = '{0}-{1}_{2}'.format(pn.get_name(), node.get_name(), field)
            parent_conditions = self.condition_keys[n]
            # print 'parent_conditions ',n, pn, parent_conditions
            conds += [ (pn, _(x),) for x in parent_conditions]

        for pn, cnd in conds:
            # print '  condition', cnd, cnd.target, 'for', pn
            v = cnd.validate(pn, node, value, field)
            # print '  ', cnd, '==', v


    def _dispatch(self, name, node, *args, **kw):
        '''
        Dispatch en event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        # print 'dispatch', name, args[0]
        if self._event is not None:

            res = self._event(name, node, *args, **kw)

            if res is not None:
                self.event_result(res)
        else:
            print 'x  ', self, "Error on _event existence"

    def event_result(self, flag, result, handler):
        if flag is False:
            raise result

    def get_conditions(self, node, name, value=None):
        '''
        Get conditions based upon node and name
        '''
        n = node
        if hasattr(n, 'get_name'):
            n = node.get_name()
        cn = '{0}_{1}'.format(n, name)

        cnds = self.conditions
        ks = self.condition_keys
        # print 'get_conditions', n, cn, value
        # exact match string
        res = []
        if value is not None:
            vcn = '{0}_{1}_{2}'.format(n, name, value)
            res += self.get_conditions_by_name(vcn) or []

        # get sub tree and validate

        vcn = '{0}_{1}'.format(n, name)
        res += self.get_conditions_by_name(vcn) or []

        # print cnds, ks
        return set(res)

    def get_conditions_by_name(self, name):
        '''
        return the conditions matching a name provided.
        '''
        cnds = self.conditions
        ks = self.condition_keys

        # print 'get_condition_by_name', name
        res = []
        if name in ks:
            vs = ks[name]
            if isinstance(vs, (list, tuple,)):
                for v in vs:
                    res.append(cnds[v])
            else:
                res.append(cnds[vs])
        return res

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
