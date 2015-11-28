import Pyro4
from bridge import Bridge


class BaseAdapter(object):
    '''
    An adapter for all future adapters to extend
    '''
    connections = None
    name = None

    def __init__(self, name, item=None, bridge=None):
        self.connections = {}
        self.name = name
        self.item = item
        self.bridge = bridge or Bridge(self)

    def get_object(self, uri):
        return uri

    def add(self, name, uri):
        '''
        Add a remote peer to the connection pool
        '''
        self.connections[name] = uri
        return name
        # Cache by any ref

    def send(self, key, *args, **kw):
        '''
        Send a call to the remote connections for method key, passing
        *args and **kw
        '''
        res = {}
        for name in self.connections:
            v = self.send_to(name, key, *args, **kw)
            res[name] = v
        return res

    def send_to(self, name, key, *args, **kw):
        '''
        call a remote object by connection name.
        '''
        uri = self.connections[name]
        print 'sending to', name, key
        o = self.get_object(uri)
        v = o.call(key, *args, **kw)
        print 'Result', v
        return v

    def node_event(self, event, *args, **kw):
        '''
        Called by the internal self.bridge, this method is passed values
        of an event captured from the network.
        The first argument 'event' is the name of the event followed by its
        arguments in order.
        the kw arguments are values matching the event.
        node and machine in kw denote the original event data.
        '''
        print 'adapter', event, args, kw
        originator = kw.get('machine', None)
        # peer back.
        print 'Peering:     Not to', originator, self.connections.keys()
        for name in self.connections:
            if name != originator:
                self.send_to(name, 'node_event', event, *args, **kw)
        # condition react
        if self.item is not None:
            self.call_item(event, *args, **kw)

    def call_item(self, event, *args, **kw):
        '''
        Call the attached item (most likely a Machine), cleaning the
        attributes to call the machine.node_event
        '''
        originator_node = kw.get('node', None)
        if 'node' in kw:
            del kw['node']
        # if 'machine' in kw:
        #     del kw['machine']

        if event == 'set':
            self.item.node_set_event(args[0], args[1], args[2], node=originator_node)

    def __getitem__(self, name):
        return getattr(self.bridge, name)

    def __getattr__(self, name):
        '''
        Calling an adapter in a functional way returns the bridge
        '''
        if hasattr(self.bridge, name):
            return getattr(self.bridge, name)
        return None


class PyroAdapter(BaseAdapter):
    '''
    A PyroAdapter uses Pyro4 to dispatch events throguh
    a peer network. A daemon is setup and
    an RPC object is exposed.
    '''

    def __init__(self, name, item=None, bridge=None):
        '''
        Pass through for the BaseAdapter, setting None for future
        values _daemon and uri
        '''
        self._daemon = None
        self.uri = None
        self._objects = {}
        super(PyroAdapter, self).__init__(name, item, bridge)

    def setup(self):
        '''
        Perform a setup of the Pyro4 library. Copy attributes as config
        from .config to Pyro4.config
        '''
        import config as _c
        _k = [x if x.startswith('__') is False else None for x in dir(_c)]
        keys = filter(None, _k)
        for name in keys:
            setattr(Pyro4.config, name, getattr(_c, name))

    def daemon(self):
        '''
        Return an instance of the daemon Pyro4 uses to communicate through.
        If self._daemon is None a new Pyro4.Daemon is created.
        self.setup() is called before the Daemon is created.
        Returned is an instance of the daemon.
        '''
        if self._daemon is None:
            self.setup()
            self._daemon = Pyro4.Daemon()
        return self._daemon

    def register(self, item):
        '''
        Register the item using Pyro4 daemon register. returned is the
        Pyro4 register object (a URI)
        '''
        if self._daemon is None:
            self.daemon()
        return self._daemon.register(item)

    def get_nameserver(self):
        '''
        Use Pyro4 to locate and return the nameserver.
        If the daemon does not exist self.setup() will be called.
        Returned is an instance of the Pyro4 Nameserver or None.
        '''
        if self._daemon is None:
            self.setup()
        try:
            return Pyro4.locateNS()
        except Pyro4.errors.NamingError:
            # no name server
            return None

    def get_object(self, uri):
        '''
        Resolve a Pyro4 uri object to a Pyro4.Proxy object.
        returned is a proxy object (a remote Bridge instance)
        '''
        o = Pyro4.Proxy(uri)
        return o

    def generate(self, bridge=None):
        b = bridge or self.bridge
        b.parent = self
        uri = self.register(b)
        return (uri, b,)

    def get_uri(self, bridge=None):
        if self.uri is None:
            res = self.generate(bridge)
            self.uri = res[0]
        return self.uri

    def wait(self, bridge=None):
        '''
        Start the daemon request loop to receive remote actions
        This method will print the URI, resolving the adapter bridge if
        it has not occured yet.
        '''
        uri = self.get_uri(bridge)
        print 'Wait on', uri
        self.daemon().requestLoop()


class AdapterMixin(object):
    '''
    Easy handler of the adapter
    '''
    def make_adapter(self, name=None, bridge=None):
        name = name or self.name
        return PyroAdapter(name, self, bridge)
