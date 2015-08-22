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

    def __init__(self, machine):
        self.machine = machine

    def machine_event(self):
        print 'Connection heard', args

    def create(self):
        print 'perform connection'
        m = self.machine
        b = Bridge(m)
        d = Pyro4.Daemon()
        uri = d.register(b)
        ns = Pyro4.locateNS()
        n = 'machine.{0}'.format(m.name)
        ns.register(n, uri)
        print 'URI', n, '::', uri

        self.uri = uri
        self.bridge = b
        self.daemon = d

        return b
        # Does this connection exist?
        #   Join
        # else Create and join

    def connect(self, uri):
        o = Pyro4.Proxy(uri)
        return o

    def resolve(self, name):
        '''
        resolve a name from the network
        '''
        ns = self.get_nameserver()
        r = ns.lookup(name)
        return str(r)

    def get_nameserver(self):
        return Pyro4.locateNS()


    def wait(self):
        '''
        Start the daemon listener
        '''
        try:
            self.daemon.requestLoop()
        except KeyboardInterrupt as e:
            print 'Stop remote listening'

