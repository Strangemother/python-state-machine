import Pyro4
from axel import Event

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
        b = Bridge(m)
        d = Pyro4.Daemon()
        uri = d.register(b)
        ns = self.get_nameserver()

        if ns is not None:
            n = 'machine.{0}'.format(m.name)
            ns.register(n, uri)
            print 'URI', n, '::', uri
        else:
            print 'URI (no NS)', uri

        self.uri = uri
        self.bridge = b
        self.daemon = d
        self._created = True
        return b
        # Does this connection exist?
        #   Join
        # else Create and join

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
        try:
            return Pyro4.locateNS()
        except Pyro4.errors.NamingError as e:
            # no name server
            return None


    def wait(self):
        '''
        Start the daemon listener
        '''
        try:
            self.daemon.requestLoop()
        except KeyboardInterrupt as e:
            print 'Stop remote listening'

