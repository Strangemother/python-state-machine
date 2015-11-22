from time import time as _time


class MethodPointer(object):
    '''
    A ping/pong calling strategy. Call the
    pointer method of which returns a string
    of a second method.

        MethodPointer().ping()
        # foo
        MethodPointer().foo(*args)
        # result

    This class is used for bridging network
    requests. The ping method is used to
    chack for alive. The ping() method can
    return a result for an 'info' method.

    This will save on method names and is handy
    for remote heartbeats on agnostic network nodes.
    '''

    def __init__(self):
        self._start_time = int(_time())

    def call(self, method_name, *args, **kw):
        '''
        Call a method on this bridge returning the expected functional
        values.
        '''
        if method_name in self.keys():
            m = getattr(self, method_name)
            return m(*args, **kw)
        return False

    def __getitem__(self, name):
        return getattr(self, name)

    def keys(self):
        '''
        Return a list of keys available on this bridge
        '''
        cdir = dir(self.__class__)
        l = [x if x.startswith('_') is False else None for x in cdir]
        return filter(None, l)

    def ping(self):
        '''
        Simple ping method. Returning a pointer to
        a greater method.
        '''
        return 'info'

    def info(self):
        return 'ping'


class Bridge(MethodPointer):
    '''
    A Bridge is presented on the network for other Machines to call. 
    The RPC layer will expose an instance of this class as methods
    to call. 
    All methods are relative to the host Machine. 
    '''
    parent = None

    def __init__(self, parent=None):
        if parent:
            self.parent = parent
        super(Bridge, self).__init__()

    def foo(self):
        print 'foo'

    def name(self):
        return self.parent.name

    def add_peer(self, name, uri):
        print 'received peer', name, uri
        self.parent.add(name, uri)
        return True

    def peers(self):
        '''
        return a list of peers assigned to this bridge.
        '''
        return self.parent.connections

    def info(self):
        '''
        Return information about this runnning machine instance.
        '''
        n = self.parent.name
        st = self._start_time
        print 'someone asked for information'
        return {
            'name': n,
            'start_time': st,
        }

    def node_event(self, event, *args, **kw):
        return self.parent.node_event(event, *args, **kw)

