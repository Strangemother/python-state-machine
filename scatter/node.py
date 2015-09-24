'''
A Node is the endpoint to the API, exposed to integrate into your
logic. Defining a class extending Node class provides a dispatch routine
when integrated to a Machine.
The Machine monitors a Node - or more precisely, monitors Node._event
with a callback.
A node is a very simple object designed to be lightweight for maximum
pliability. The Machine handles the heavy load.
'''

import inspect
from axel import Event


class Conditions(object):
    '''
    A Mixin construct to assist in applying and managing conditions.
    '''
    _conditions = ()

    def conditions(self):
        '''
        Returns a list of conditions to meet.
        '''
        if hasattr(self, '_conditions'):
            if hasattr(self, 'get') and self.get is not None:
                return self.get('_conditions')
            else:
                return self._conditions
        return ()


class GetSetMixin(object):
    '''
    Provide a entry point for monitoring the change in
    the monitored variables.
    '''

    def watch(self, node, names):
        '''
        Provide a node and a list of variables to monitor.
        '''
        for name in names:
            self.monitor_key(node, name)

    def monitor_key(self, node, name):
        '''
        watch events to changes of the supplied named key
        on the provided node.
        '''
        def delx(self):
            print "+++ delx()"
            # del self.__x

        def proxy_get(self, k):
            print 'proxy get', k

        def proxy_set(self, k):
            print 'proxy set', k

        print 'monitor', name

    def get(self, k):
        '''
        return an attribute from this node
        '''
        if k in self.__dict__:
            v = self.__dict__[k]
            return v
        # self.fetch_get(k)
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            pass
        return None

    def set(self, k, v):
        '''
        Change an attribute on this node
        '''
        # import pdb;pdb.set_trace()
        # setattr(self.__dict__, k, v)
        # print 'set', k, v
        self.__dict__[k] = v
        # print 'dict', self.__dict__
        return self.get(k)


class MachineIntegration(object):
    _event = None

    def _build_event(self):
        print '^  ', self, 'create event'
        self._event = Event(self)

    def _dispatch(self, name, *args, **kw):
        '''
        Dispatch en event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        # print 'dispatch', name, args[0]
        if self._event is not None:
            res = self._event(name, *args, **kw)
            self.event_result(*res[0])
        else:
            print 'x  ', self, "Error on _event existence"

    def event_result(self, flag, result, handler):
        if flag is False:
            raise result


class NodeObject(Conditions, MachineIntegration):

    def __init__(self, name=None):
        '''
        The init method has very little to do (hopefully less)
        the self._event is instantiated for Machine callback.
        This should be taken off the __init__ eventually.
        '''
        self.name = name
        self._build_event()

    def get_name(self):
        '''
        Get the name of the Node, defaulting to the class name if
        name is None.
        Return is the name of this node to be integrated into a Machine
        and it's network.
        '''
        if self.name is None:
            return self.__class__.__name__
        return self.name

    def __str__(self):
        c = self.name or self.__class__.__name__
        return str('Node "{0}"'.format(c))

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.get_name(),
        }

        return '<nodes.Node:{cls_name}("{name}")>'.format(**kw)


class Node(NodeObject, GetSetMixin):
    pass


class TestNode(object):

    _event = None

    def __init__(self):
        self._build_event()

    def get_name(self):
        return 'TestNode'

    def _build_event(self):
        print '^  ', self, 'create event'
        self._event = Event(self)
