from tools import color_print as cl


class ConditionIntegrate(object):

    def read_node(self, node):
        '''
        Read the conditions of a node.
        '''
        if hasattr(node, 'conditions') is False:
            return
        cnds = node.conditions()
        # cl('yellow', 'get conditions for node', node)
        self.integrate_conditions(cnds, node)

    def integrate_conditions(self, conditions, node):
        '''
        Implement a list of conditions against one node.
        '''
        for c in conditions:
            self.integrate_condition(c, node)

    def integrate_condition(self, cond, node):
        '''
        Integrate the conditions into the condition runner
        '''
        if hasattr(self, 'condition_keys') is False:
            setattr(self, 'condition_keys', {})

        if hasattr(self, 'condition_nodes') is False:
            setattr(self, 'condition_nodes', {})

        names = self.get_integration_names(node, cond)
        # cl('yellow', 'integrate conditions', node, cond, names)
        self.append_with_names(names, cond)
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

    def run_conditions(self, conditions, node, value, field):
        # pprint(self.conditions._names)
        # cl('yellow', 'run conditions', conditions, node, field)
        pairs = []
        # fetch associated conditions.
        # make the condition perform the compare
        for cond in conditions:
            # get associated nodes for the condition
            node_names = self.condition_keys.get(str(cond)) or []
            # loop and get associated condition
            for nn in node_names:
                s = '{0}-{1}'.format(nn, str(cond))
                r = self.get(s) or []
                f = [(self.nodes.get(nn), set(r),)]
                # cl('yellow', 'found', f)
                pairs.extend( f )

        res = {}
        for parent_nodes, _conditions in pairs:
            for cnd in _conditions:
                for pn in parent_nodes:
                    v = cnd.validate(pn, node, value, field)
                    n = '{0}-{1}'.format(pn.get_name(), str(cnd))
                    res[n]= v
        # cl('blue', 'conditions', res)
        return res

    def find_conditions(self, node, field, value):
        n = '{0}_{1}_{2}'.format(node.get_name(), field, value)
        # print '+  find conditions on', n
        cnds = self.get_conditions(node, field, value)
        # cl('yellow', '-- Matches condition', cnds)
        return cnds

    def get_conditions(self, node, name, value=None):
        '''
        Get conditions based upon node and name
        '''
        node_name = node
        cl('red', 'get condition', node, name, value)
        cnds = self.conditions

        if hasattr(node_name, 'get_name'):
            node_name = node.get_name()
        name1 = '{0}_{1}'.format(node_name, name)

        match_names = (name1, )

        # exact match string
        if value is not None:
            vcn = '{0}_{1}_{2}'.format(node_name, name, value)
            match_names += (vcn,)

        res = []
        for _n in match_names:
            res += self.get_conditions_by_name(_n) or []
        # print 'found conditions', res
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

