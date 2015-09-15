from axel import Event
from node import NodeObject, Node, MachineIntegration


class ProxyBase(object):
    _address = None

    def set_address(self, v):
        self._address = v

    def get_address(self):
        return self._address

    address = property(get_address, set_address)


class Proxy(NodeObject, ProxyBase, MachineIntegration):
    '''
    A Proxy machine maintains an active connection
    through a bridge calling methods through the
    local machine to the target machine.
    You could send events through your local machine -
    but it's easier to use a Proxy type.
    '''

    def get_name(self):
        return str(self.address)


class ProxyNode(Proxy):
    '''
    A proxy node simulates node calls on a remote object.
    '''
    _classive = Proxy

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.get_name(),
        }

        return '<nodes.ProxyNode:{cls_name}("{name}")>'.format(**kw)

    def set(self, k, v):
        '''
        Set an attribute to the node and dispatch an event handled by the
        Machine to inform the network. This is wrapped by the __setattr__
        allowing property() changes to be perpetuated.
        return is the result of the super call to set()
        '''
        # print 'node', self, k,v
        if self.react is True:
            ov = self.get(k)
            self._dispatch('set', k, v, ov)
        return super(ProxyNode, self).set(k,v)

    def __getattr__(self, key):
        '''
        capture attributes of which do not exist - dispatching
        a request through the machine to the self address.
        '''
        print 'get', key

        return object.__getattribute__(self, key)

    def __setattr__(self, key, v):
        print 'set', key
        return object.__setattr__(self, key, v)

    # def __getattribute__(self, key):
    #     v = object.__getattribute__(self, key)
    #     if v is None:
    #         v = object.__getattribute__(self,'get')(key)
    #     return v
