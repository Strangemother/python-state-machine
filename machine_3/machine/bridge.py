import Pyro4
from axel import Event
from tools import color_print as cl

class Bridge(object):

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


class PyroAdapter(object):

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
            return Pyro4.locateNS()
        except Pyro4.errors.NamingError as e:
            # no name server
            return None


class Connection(object):

    def __init__(self, machine, peers=None):
        self.machine = machine
        self._created = False
        self.peers = peers or []
        self._resolved_peers = {}

    def machine_event(self):
        print 'Connection heard', args

    def create(self):
        print 'perform connection'
        m = self.machine
        b, a, d, uri = self.create_bridge(m)
        self.uri = uri
        self.bridge = b
        self.daemon = d
        self.adapter = a
        self._created = True
        return b

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
            n = 'machine.{0}'.format(m.name)
            ns.register(n, uri)
            cl('red', 'URI', n, '::', uri)
        else:
            cl('red', 'URI (no NS)', uri)

        return (b, a, d, uri)


    def set(self, name, field, value, value_from):
        '''
        Set a value on the network
        '''
        print 'connection set', name, field, value, value_from
        if self._created is False:
            b = self.create()
        else:
            b = self.bridge

        if b is not None:
            print 'sending on', b
            # self.machine.event_set(name, field, value)
            return self.dispatch_set(name, field, value)
        else:
            print 'did not dispatch value', field
        return True

    def dispatch_set(self, name, field, value):
        '''
        Tell all peers
        '''
        peers = self.resolve_peers()
        #print 'dispatching to peers', peers
        for machine in peers:
            proxy = peers[machine]
            # print 'dispatch to name', name, proxy
            n = name.get_name() if hasattr(name, 'get_name') else name
            proxy.set(n, field, value)

    def connect(self, uri):
        o = Pyro4.Proxy(uri)
        return o

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
