import Pyro4
from axel import Event
from tools import color_print as cl


class Bridge(object):
    '''
    A bridge is served by your running machine and called by
    remote procedure.
    '''

    def __init__(self, machine):
        self.machine = machine

    def get_name(self):
        '''
        return the name from this
        bridge machine instance.
        '''
        print 'bridge get_name'
        return self.machine.name

    def set(self, node_name, key, value):
        print 'Bridge set', node_name, key, value
        self.machine.set_on_node(node_name, key, value)
        return True

    def get_nodes(self, name=None):
        print 'Fetch from bridge::', name
        r = []
        for node in self.machine.get_nodes(name):
            t= 'node'
            s= '%s.%s.%s' % (t, self.machine.name, node.get_name(), )
            r.append(Address(s))
        return r

    def add_peer(self, uri):
        print 'Bridge adding peer', uri
        self.machine.add_peer(uri)
        return (uri in peers)

    def ping(self):
        '''
        Return useful (cheap) pointer to the member associating
        machine information.
        '''
        print '!Pong.'
        return 'info'

    def info(self):
        '''
        Return information about this runnning machine instance.
        '''
        n = self.machine.name
        st = self.machine._start_time
        print 'someone asked for information'
        return {
            'name': n,
            'start_time': st,
        }

    def call(self, method_name, *args, **kw):
        '''
        Call a method on this bridge returning the expected functional
        values.
        '''
        if method_name in self.keys():
            m = getattr(self, method_name)
            return m(*args, **kw)
        return False

    def keys(self):
        '''
        Return a list of keys available on this bridge
        '''
        cdir = dir(self.__class__)
        l = [x if x.startswith('_') is False else None for x in cdir]
        return filter(None, l)


class PyroAdapter(object):

    _nameserver = False

    def __init__(self):
        self._daemon = None

    def setup_pyro(self):
        import config as _c
        _k = [x if x.startswith('__') is False else None for x in dir(_c)]
        keys = filter(None, _k)
        for name in keys:
            setattr(Pyro4.config, name, getattr(_c,name))

    def daemon(self):
        if self._daemon is None:
            self.setup_pyro()
            self._daemon = Pyro4.Daemon()
        return self._daemon

    def register(self, item):
        if self._daemon is None:
            self.daemon()
        return self._daemon.register(item)

    def get_nameserver(self):
        if self._daemon is None:
            self.setup_pyro()
        try:
            if self._nameserver is True:
                return Pyro4.locateNS()
        except Pyro4.errors.NamingError as e:
            # no name server
            return None

    def get_object(self, uri):
        o = Pyro4.Proxy(uri)
        return o


class Connection(object):

    def __init__(self, machine, peers=None):
        self.machine = machine
        self._created = False
        self.peers = peers or []
        self._resolved_peers = {}
        self.peer_alias = {}

    def machine_event(self):
        cl('yellow', 'Connection heard', args)

    def create(self):
        cl('yellow', 'perform connection')
        m = self.machine
        b, a, d, uri = self.create_bridge(m)
        self.uri = uri
        self.bridge = b
        self.daemon = d
        self.adapter = a
        self._created = True
        return b

    def ready(self):
        if self._created is False:
            self.create()
        return True

    def create_bridge(self, machine):
        '''
        Create a bridge for the machine to communicate though.
        When changes occur to a node, the machine dispatches this as
        an event though the bridge.
        '''
        b = Bridge(machine)
        a = PyroAdapter()
        d = a.daemon()
        uri = a.register(b)
        ns = a.get_nameserver()

        if ns is not None:
            n = 'machine.{0}'.format(machine.name)
            ns.register(n, uri)
            cl('red', 'Bridge', n, '::', uri)
        else:
            cl('red', 'Bridge (no NS)', uri)

        return (b, a, d, uri)

    def get_bridge(self):
        if self._created is False:
            b = self.create()
        return self.bridge

    def get_adapter(self):
        if self._created is False:
            b = self.create()
        return self.adapter

    def get_peers(self):
        peers = self.resolve_peers().values()
        return peers

    def send(self, name, *args, **kwargs):
        #print 'dispatching to peers', peers
        peers = self.get_peers()
        res = {}
        for proxy in peers:
            # print 'dispatch to name', name, proxy
            meth = getattr(proxy, name)
            if meth is None:
                cl('red', 'bridge does not support {0} event'.format(name))
            else:
                n = proxy.get_name()
                v = meth(*args, **kwargs)
                res[n] = v
        return res

    def set(self, name, field, value, value_from):
        '''
        Set a value on the network
        '''

        b = self.get_bridge()

        if b is not None:
            cl('green', 'sending on', b, name, field)
            # self.machine.event_set(name, field, value)
            return self.dispatch_event('set', name, field, value)
        else:
            cl('red', 'did not dispatch value', field)

        return True

    def dispatch_event(self, event_name, name, field, value):
        '''
        Tell all peers
        '''
        peers = self.resolve_peers()
        #print 'dispatching to peers', peers
        for machine in peers:
            proxy = peers[machine]
            # print 'dispatch to name', name, proxy
            n = name.get_name() if hasattr(name, 'get_name') else name
            _bridge_method = getattr(proxy, event_name)
            if _bridge_method is None:
                cl('red', 'bridge does not support {0} event'.format(event_name))
            else:
                _bridge_method(n, field, value)

    def connect(self, uri):
        '''
        Connect to a remote machine
        '''
        machine = self.get_adapter().get_object(uri)
        ping = machine.ping()
        info = machine.call(ping)
        self.peer_alias[info['name']] = uri
        return machine

    def resolve_peers(self):
        for p in self.peers:
            _p = self._resolved_peers.get(p)
            if _p is None:
                self._resolved_peers[p] = self.connect(p)
        return self._resolved_peers

    def resolve_name(self, name):
        '''
        resolve a name from the network
        '''
        ns = self.get_nameserver()
        r = ns.lookup(name)
        return str(r)

    def get_nameserver(self):
        self.adapter.get_nameserver()

    def wait(self):
        '''
        Start the daemon listener
        '''
        try:
            self.daemon.requestLoop()
        except KeyboardInterrupt as e:
            print 'Stop remote listening'
