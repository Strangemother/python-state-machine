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

    def get_parent(self):
        if self.parent is not None:
            return self.parent
        return None

    def __init__(self, parent=None, node_event=None):
        if parent:
            self.parent = parent
            self.name = self.parent.name
        self._event_handler = node_event
        print 'bridge node event', node_event
        super(Bridge, self).__init__()

    def name(self):
        return self.name

    def add_peer(self, name, uri):
        print 'received peer', name, uri
        parent = self.get_parent()
        parent.add(name, uri)
        return True

    def info(self):
        '''
        Return information about this runnning machine instance.
        '''

        n = self.name
        st = self._start_time
        print 'someone asked for information'
        return {
            'name': n,
            'start_time': st,
        }

    def node_event(self, event, *args, **kw):
        print 'bridge node_event', event, args, kw
        if self._event_handler is not None:
            print 'calling bridge node_event handler', event, args, kw
            self._event_handler(event, *args, **kw)
        parent = self.get_parent()
        if parent is not None:
            return parent.node_event(event, *args, **kw)


class BridgeMixin(object):
    '''
    A Mixin to assist with handling a Bridge and its event.
    '''

    def make_bridge_manager(self, Manager_class=None, event_handler=None):
        event_handler = event_handler or self._bridge_event
        return Manager_class(event_handler)

    def _bridge_event(self, manager, event, *args, **kw):
        print '\nbridge manager saw event', event, args, kw
        if event == 'integrate':
            item.add_peer(self.name, self.bridge)

    def make_bridge(self):
        return Bridge(self, self._bridge_node_event)

    def _bridge_node_event(self, event, *args, **kw):
        '''
        A peer has called the bridge.
        '''
        originator = kw.get('machine', None)
        originator_node = kw.get('node', None)
        if 'node' in kw:
            del kw['node']
        # if 'machine' in kw:
        #     del kw['machine']
        print '_bridge_node_event', self, event, args, kw
        if event == 'set':
            self.node_set_event(args[0], args[1], args[2],
                                node=originator_node,
                                machine=originator)
