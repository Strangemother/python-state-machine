'''
A Node is the endpoint to the API, exposed to integrate into your
logic. Defining a class extending Node class provides a dispatch routine
when integrated to a Machine.
The Machine monitors a Node - or more precisely, monitors Node._event
with a callback.
A node is a very simple object designed to be lightweight for maximum
pliability. The Machine handles the heavy load.
'''
from mixins import GetSetMixin, NameMixin, EventMixin, ConditionsMixin
from managers import NodeManager


class Node(NameMixin, ConditionsMixin, GetSetMixin, EventMixin):
    '''
    A node is simply an object of which dispatches it's value changes through
    a single member. By inheriting the GetSetMixin all none existent attributes
    are perpetuated through `get`. All applied changes to keys are pass through
    `set`
    If __getattr__ key is defined the local value is provided.
    '''

    def __init__(self, name=None):
        '''
        The init method has very little to do (hopefully less)
        the self._event_handlers is instantiated for Machine callback.
        This should be taken off the __init__ eventually.
        '''
        self._build_event()
        self._name = name

    def set(self, k, v):
        self._dispatch('set', k, v)
        valid = self._run_conditions(k, self.get(k), v, self)
        super(Node, self).set(k, v)
        super(Node, self).set('_valid', valid)

