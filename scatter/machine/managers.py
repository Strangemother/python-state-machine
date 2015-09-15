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

    def get(self, name, default=None):
        try:
            return self._names[name]
        except KeyError as e:
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
        return ( self.get_item_name(item), )


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

        except TypeError, te:
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


class NodeManager(Manager):

    def get_item_name(self, item):

        return item.get_name()
