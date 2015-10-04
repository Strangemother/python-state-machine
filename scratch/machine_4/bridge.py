from axel import Event
from tools import color_print as cl
from address import Address
from proxy import ProxyMachine


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
            print 'found node', node
            t = 'node'
            s = '%s.%s.%s' % (t, self.machine.name, node.get_name(), )
            r.append(str(Address(s)))
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


class Peers(list):

    def __init__(self, machine):
        self.machine = machine
        self._created = False
        self._resolved_peers = {};

    def add_string(self, address_string):
        '''
        Add a peer to the set first casting a string into a machine type
        '''
        machine = ProxyMachine(address_string)
        self.add(machine)
        return machine

    def add(self, machine):
        '''
        Add the string to the peers and resolve
        '''
        self.append(machine)
        self.resolve(machine)
        return machine

    def get_resolved(self):
        peers = self.resolve_peers().values()
        return peers

    def resolve(self, peer=None):
        '''
        Resolve all peers in list of which are not resolved.
        If a peer string is not passed all unresolved peers are
        resolved.
        '''
        if peer is not None:
            self.resolve_peer(peer)
        else:
            self.resolve_peers()

    def resolve_peer(self, machine):
        '''
        Connect and resolve the peer object. returning a machine
        type.
        '''
        return self.connect(machine)

    def connect(self, machine):
        print 'connect', machine

    def resolve_peers(self):
        '''
        Resolve all peers in self.peers of which are not connected
        All peers not resolved will call self.connect returning a
        machine type.
        '''

        for addr in self:
            # already resolved peers have an associate
            _p = self._resolved_peers.get(addr)
            if _p is None:
                # perform a connection
                self._resolved_peers[addr] = self.connect(addr)
        return self._resolved_peers

    def add_peer(self, string):
        self._bridged = True
        self.append(string)
        self.resolve_peers()
