'''
A collection of generic mixins for Node, Conditions and Machine
integration
'''
from axel import Event


class NameMixin(object):
    '''
    Provides a method to receive a name of the class.
    If the _name is undefined __class__.__name__ is default return.
    '''

    _name = None

    def __get_class(self):
        '''
        return the target class. Self.
        '''
        return self.__class__

    def get_name(self):
        '''
        Get the name of the Node, defaulting to the class name if
        name is None.
        Return is the name of this node to be integrated into a Machine
        and it's network.
        '''
        if self._name is None:
            return self.__get_class().__name__
        return self._name

    def __str__(self):
        c = self.get_name()
        return str('Node "{0}"'.format(c))

    def __repr__(self):
        __class = self.__get_class()

        kw = {
            'module': __class.__module__,
            'cls_name': __class.__name__,
            'name': self.get_name(),
        }

        return '<{module}:{cls_name}("{name}")>'.format(**kw)


class GetSetMixin(object):

    def get(self, k):
        '''
        return an attribute from this node
        '''
        # print 'get', k
        # self.fetch_get(k)
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            pass
        return None

        if k in self.__dict__:
            v = self.__dict__[k]
            return v

    def set(self, k, v):
        '''
        Change an attribute on this node
        '''
        # setattr(self.__dict__, k, v)
        print 'set', k, v
        self.__dict__[k] = v
        # print 'dict', self.__dict__
        return self.get(k)

    def __getattr__(self, key):
        '''
        capture attributes of which do not exist - dispatching
        a request through the machine to the self address.
        '''
        return self.get(key)

    def __setattr__(self, key, v):
        return self.set(key, v)


class EventMixin(object):
    _event_handlers = None

    def _build_event(self):
        self._event_handlers = Event(self)

    def _dispatch(self, name, *args, **kw):
        '''
        Dispatch en event for the Machine to handle. This should
        be lightweight string data hopefully.
        If the internal ._event is missing an error will occur.
        '''
        if self._event_handlers is not None:
            print 'dispatch', name, args[0]
            res = self._event_handlers(name, *args, **kw)
            if res is not None:
                self.event_result(*res[0])
        else:
            print 'x  ', self, "Error on _event existence for", name

    def event_result(self, flag, result, handler):
        if flag is False:
            raise result
