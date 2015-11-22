from bridge import Bridge
from adapters import PyroAdapter
from tools import color_print as cl
from tools.daemon import Daemon


class Connection(object):
    adapterClass = None

    def __init__(self, machine, peers=None):
        self.machine = machine
        self._created = False
        self.peers = peers or []
        self._resolved_peers = {}
        self.peer_alias = {}

    def machine_event(self):
        cl('yellow', 'Connection heard')

    def create(self):
        cl('yellow', 'perform connection')
        m = self.machine
        self.create_bridge(m)
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
        self.adapter_setup(self, b)
        return b

    def get_bridge(self):
        '''
        Return the bridge connection - if a connection has not been created,
        self.create() is called.
        '''
        if self._created is False:
            self.create()
        return self.bridge

    def adapter_setup(self, bridge):
        '''
        setup the bridge through the attached provider.
        '''
        if self.adapterClass is not None:
            return self.adapterClass(b)
        return None

    def get_adapter(self):
        '''
        Return an instance of the adapter connection - if a connection has not
        been created, self.create() is called.
        '''
        if self._created is False:
            self.create()
        return self.adapter

    def get_object(self, name):
        '''
        Return an object from the connected class.
        '''
        return None

    def get_peers(self):
        peers = self.resolve_peers().values()
        return peers

    def send(self, name, *args, **kwargs):
        # print 'dispatching to peers', peers
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
        # print 'dispatching to peers', peers
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
        machine = self.get_object(uri)
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
        return self.adapter.get_nameserver()


class DaemonConnection(Connection):

    def daemon(self):
        pidfile = './machine.{0}.pid'.format(self.machine.name)
        _d = Daemon(pidfile)
        _d.run = self.run
        return _d

    def run(self):
        self.ready()
        self.loop()

    def loop(self):
        try:
            self.wait()
        except KeyboardInterrupt:
            cl('red', 'kill')

    def wait(self):
        '''
        Start the daemon listener
        '''

        try:
            self.daemon.requestLoop()
        except KeyboardInterrupt:
            print 'Stop remote listening'

    def create(self):
        cl('yellow', 'perform connection')
        self.daemon = self.daemon()
        return b


class PyroConnection(Connection):
    adapterClass = PyroAdapter

    def get_object(self, name):
        '''
        Return an object from the connected class.
        '''
        return self.get_adapter().get_object(name)

    def adapter_setup(self, bridge):
        '''
        setup the bridge through the attached provider.
        '''
        self.adapter = self.adapterClass()
        # self.daemon = self.adapter.daemon()
        self.uri = self.adapter.register(bridge)
        ns = self.adapter.get_nameserver()

        if ns is not None:
            n = 'machine.{0}'.format(bridge.machine.name)
            ns.register(n, uri)
            cl('red', 'Bridge', n, '::', uri)
        else:
            cl('red', 'Bridge (no NS)', uri)

        return (bridge, self.adapter, self.uri)
