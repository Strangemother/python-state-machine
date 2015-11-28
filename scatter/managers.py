from axel import Event


class Manager(list):

    def __init__(self, event_callback=None):
        self._names = {}
        self._event = Event(self)
        if event_callback is not None:
            self._event += event_callback

    def __contains__(self, key):
        # print '__contains__', key, self.node_names
        if key in self._names:
            return True
        return super(Manager, self).__contains__(key)

    def __getitem__(self, key):
        if isinstance(key, int):
            return list.__getitem__(self, key)
        return self._names[key]

    def __getattr__(self, key):
        '''
        return a list of objects matching the name provided.
        '''
        return self.get(key)

    def get(self, name, default=None):
        try:
            return self._names[name]
        except KeyError:
            return default

    def append(self, *args):
        super(Manager, self).append(*args)
        for n in args:
            sref = self.integrate_item(n)
            self._append(sref, n)

    def append_with_names(self, names, *args):
        super(Manager, self).append(*args)
        for item in args:
            ref = self.integrate_item(item, names)
            self._append(ref, item)

    def get_item_name(self, item):
        return item

    def get_item_names(self, item):
        return (self.get_item_name(item), )

    def integrate_item(self, node, names=None):
        n = self.get_item_name(node)
        if (n in self._names) is False:
            self._names[n] = []

        try:
            name_iter = iter(names)
            for alias in name_iter:
                # run alias names into the cache
                if (alias in self._names) is False:
                    self._names[alias] = []
                self._names[alias].append(node)
                # Create sub string for alias names.
                _names = self.get_item_names(node)
                # now iter build names with aliases.
                for n in _names:
                    s = '{0}-{1}'.format(alias, n)
                    # append sub string name to cache.
                    if (s in self._names) is False:
                        self._names[s] = []
                    self._names[s].append(node)
        except TypeError:
            pass
        return n

    def _append(self, name, item):
        self._names[name].append(item)
        self._event('integrate', item, name=name)
        return item


class ConditionsManager(Manager):

    def get_item_names(self, item):
        watch_name = item.watch

        _t = item.target
        if isinstance(item.target, tuple):
            _t = hash(item.target)
        tp = (
            watch_name,
            '{0}_{1}'.format(watch_name, item.field),
            '{0}_{1}_{2}'.format(watch_name, item.field, _t),
            '{0}_{1}_{2}'.format(watch_name, item.field, item.target),
            )

        return tp

    def integrate_item(self, item, names=None):
        n = self.get_item_name(item)
        ns = self.get_item_names(item)

        for name in ns:
            if (name in self._names) is False:
                if name != n:
                    self._names[name] = []
                    self._names[name].append(item)

        return super(ConditionsManager, self).integrate_item(item, names)

    def get_item_name(self, item):
        str_n = str(item)
        return str_n


class BridgeManager(Manager):

    def add(self, *args):
        return self.append(*args)

    def get_item_name(self, item):
        '''
        return a name freom the machine
        '''
        return item.name


class Events(object):

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
        Dispatch an event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        self.on_event(name, node, *args, **kw)
        # print 'dispatch', name, args[0]
        if self._event is not None:
            res = self._event(name, node, *args, **kw)

            if res is not None:
                self.event_result(res)
            return res
        else:
            print 'x  ', self, "Error on _event existence"

    def on_event(self, name, node, *args, **kw):
        pass
        # print 'EVENT', name, node

    def event_result(self, flag, result, handler):
        if flag is False:
            raise result

    def dispatch_integrate(self, node):
        return self._dispatch('integrate', node)


class NodeIntegrate(Events):

    def add(self, *args):
        '''
        add a node to the manager
        '''
        for node in args:
            # print '+   add_node', node
            self.append(node)
            self.integrate_node(node)

    def integrate_node(self, node):
        # self.read_conditions(node)
        self._add_node(node)
        # node._event += self.node_event
        # self.dispatch_integrate(node)
        node.react = True

    def get_nodes(self, node_name=None, default=None):
        '''
        return the value from a node through node search
        '''
        ns = self.get(node_name, default)
        return ns

    def set_on_node(self, node_name, key, value):
        '''
        Change the value of the nodes returned from the node_name search
        '''
        nodes = self.get_nodes(node_name)
        # print 'set_on_node', node_name, nodes
        if nodes is None:
            # print 'Machine', self, ':: No nodes', node_name
            return

        for node in nodes:
            # print 'Setting', node, key, 'to', value
            node.set(key, value)


class NodeManager(Manager, NodeIntegrate):

    def __init__(self, _add_node=None):
        self._names = {}
        self._event = Event(self)
        self._add_node = _add_node

    def node_event(self, node, name, *args, **kw):
        # print '-- Event:', str(node), name, args, kw
        # s = self.condition_name(node, name, *args, **kw)

        if name == 'set':
            self.event_set(node, *args, **kw)
        self._dispatch(name, node, *args, **kw)
        # The value has been set.
        # check the condition of other nodes.

    def get_item_name(self, item):
        return item.get_name()
