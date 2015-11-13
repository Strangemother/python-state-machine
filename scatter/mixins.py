'''
A collection of generic mixins for Node, Conditions and Machine
integration
'''
from axel import Event
from compares.const import RUNNING, CLEAR
import sys, traceback


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
        try:
            return object.__getattribute__(self, k)
        except AttributeError:
            pass
        return None

    def set(self, k, v):
        '''
        Change an attribute on this node
        '''
        # setattr(self.__dict__, k, v)
        # print 'set', k, v
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
            # print 'dispatch', name, args[0]
            res = self._event_handlers(name, *args, **kw)
            if res is not None:
                self.event_result(*res[0])
        else:
            print 'x  ', self, "Error on _event existence for", name

    def event_result(self, flag, result, handler):

        if flag is False:
            # import traceback
            # import cgitb
            # import sys
            # t, v, tb = sys.exc_info()
            # cgitb.enable(format='text')
            # import pdb; pdb.set_trace()  # breakpoint e6e8ef60 //
            raise result


class ConditionsMixin(object):
    '''
    A Mixin construct to assist in applying and managing conditions.
    '''
    _conditions = ()

    def _run_conditions(self, key, current, incoming, node=None):
        '''
        run the conditions against the differences of the key in the node
        old and new.
        '''
        cnds = self.conditions()

        if len(cnds) == 0:
            # No conditions were applied.
            return True

        validity = {}

        for cnd in cnds:
            if cnd.state == RUNNING: continue
            cnd.state = RUNNING

            try:
                v = cnd.match(current, incoming, node, key, parent_node=self)
            except Exception as exc:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                formatted_lines = traceback.format_exc().splitlines()
                # print formatted_lines
                print '\nError: {0}({2}) on {1}'.format(exc_type.__name__, self, exc_value)
                print '\n'.join(formatted_lines)
                # print '\n'.join(traceback.format_tb(exc_traceback))

                # raise exc
                v = False
            validity[key] = v
            cnd.state = CLEAR

        vlist = list(set(validity.values()))
        res = False if len(vlist) > 1 else vlist[0]
        return res

    def conditions(self):
        '''
        Returns a list of conditions to meet.
        '''
        if hasattr(self, '_conditions') and getattr(self, '_conditions') is not None:
            if hasattr(self, 'get') and self.get is not None:
                return self.get('_conditions')
            else:
                return self._conditions
        return ()

from managers import NodeManager, ConditionsManager

class NodeMixin(object):
    '''
    Mixin to assist in managing and reading Nodes in a Manager list.
    '''
    nodes = None

    def _setup_nodes(self, node_callback=None):
        '''
        Setup node handling by creating a reference to the callback
        and creating a node manager.
        '''
        self._node_callback = node_callback or self.node_event_handler
        self.nodes = NodeManager(self._add_node_event_handler)

    def _add_node_event_handler(self, node):
        '''
        Callback for a node being added to the node manager.
        '''
        # print 'NodeMixin: Add node::', node.get_name()
        node._event_handlers += self._node_callback

    def node_event_handler(self, node, *args, **kw):
        '''
        This method is provided to NodeManager manager upon instansiation
        and is called through the event library.
        '''
        import pdb; pdb.set_trace()  # breakpoint c0622778 //
        print 'NodeMixin::node_event_handler::', node, args, kw
