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
            return self.get('_conditions')
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
        except AttributeError as e:
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
        #print 'dict', self.__dict__
        return self.get(k)


class NodeBase(Conditions, GetSetMixin):
    # A must-have field
    #
    name = None
    _event = None
    react = False

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

    def __init__(self):
        '''
        The init method has very little to do (hopefully less)
        the self._event is instantiated for Machine callback.
        This should be taken off the __init__ eventually.
        '''
        # print '^  ', self, 'create event'
        self._event = Event(self)
        self.__keys = self.keys()

    def keys(self):
        return self.get_attrs()

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

    def set(self, k, v):
        '''
        Set an attribute to the node and dispatch an event handled by the
        Machine to inform the network. This is wrapped by the __setattr__
        allowing property() changes to be perpetuated.
        return is the result of the super call to set()
        '''
        if self.react is True:
            ov = self.get(k)
            if k in self.keys():
                self._dispatch('set', k, v, ov)

        return super(NodeBase, self).set(k,v)

    def get_attrs(self):
        '''
        return the fields for this nbode to be associated on the network.
        These are attributes and methods supplied to the class
        '''
        ignore = Node.__dict__.keys()
        # ignore = reduce(lambda x, y: x+y, [x.__dict__.keys() for x in iter(classes)])
        fields = []
        classes = self.__class__.__mro__
        # rint classes
        for parent_class in iter(classes):
            # print 'class', parent_class
            keys = parent_class.__dict__.keys()
            ckeys = self.__class__.__dict__.keys()
            for model_field in keys:
                is_cls = inspect.isclass(getattr(parent_class, model_field))
                is_meta = model_field == 'Meta' and is_cls
                name = model_field
                if is_meta or model_field in ignore or model_field.startswith('__'):
                    continue
                if model_field in ckeys:
                    fields.append(name)

        for field in ignore:
            name = field
            if field in ignore or field.startswith('__'):
                continue
            ignore.append(name)
        return fields

    def __str__(self):
        c = self.name or self.__class__.__name__
        return str('Node "{0}"'.format(c))

    def __repr__(self):
        kw = {
            'cls_name': self.__class__.__name__,
            'name': self.get_name(),
        }

        return '<nodes.Node:{cls_name}("{name}")>'.format(**kw)

class Node(NodeBase):
    '''
    Exposed api for integration to the network. Extend with your
    own class and provide attributes. Changes to the class attributes
    will be dispatched as events through the Machine event monitoring.

    Other nodes on the cloud waiting for the Condition of your change will
    react.
    '''

    def __setattr__(self, name, value):
        v = self.set(name, value)

    def __getattr__(self, name):
        print '__getattr__', name
        v = self.get(name)
        print 'Node get:', name, v
        return v

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        if key in self.__keys:
            return self.set(key, value)
