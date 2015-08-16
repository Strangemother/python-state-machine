class Machine(object):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    def __init__(self, name=None):
       self.name = name
       self.conditions = {}
       self.condition_keys = {}
       self.nodes = []

    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )

    def add(self, node):
        '''
        add a node to the manager
        '''
        print '+   add_node', node
        self.nodes.append(node)
        self.integrate_node(node)

    def integrate_node(self, node):
        self.read_conditions(node)
        node._event += self.node_event
        node.react = True
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
        print '+   integrate_condition', condition
        ks = self.condition_keys
        c = condition
        node_name = c.watch

        # by node name.
        if (node_name in ks) is False:
            # add list for conditions by name
            ks[node_name] = []

        # by sub string {watch}_{field}
        ss = '{0}_{1}'.format(node_name, c.field)
        if (ss in ks) is False:
            ks[ss] = []

        # Flat lit of all conditions, met with string weakref
        cnds = self.conditions
        # name used in keys and flat
        name = str(c)

        # add to flat table.
        cnds[name] = condition
        # add to many keys.
        ks[name] = name
        ks[node_name].append(name)
        ks[ss].append(name)

        print '+   Condition integrated'


    def node_event(self, node, name, *args, **kw):
        print '-- Event:', str(node), name, args, kw
        # s = self.condition_name(node, name, *args, **kw)

        if name == 'set':
            self.event_set(node, *args, **kw)

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
        for cnd in conditions:
            # make the condition perform the compare
            v = cnd.validate(node, value, field)
            print v


    def get_conditions(self, node, name, value=None):
        '''
        Get conditions based upon node and name
        '''
        n = node.get_name()
        cn = '{0}_{1}'.format(n, name)

        cnds = self.conditions
        ks = self.condition_keys

        if value is not None:
            vcn = '{0}_{1}_{2}'.format(n, name, value)
            if vcn in ks:
                return [cnds[ks[vcn]]]
            else:
                return []

        if cn in ks:
            return cnds[ks[cn]]

        if n in ks:
            return cnds[ks[n]]




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
