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
from async import EventClock


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


_v = 0

from scatter.weak import _weaks, add_weak,get_weak
from multiprocessing import Manager

clock = None

class ClockNode(Node):

    ticks = 0

    def __init__(self, name=None):
        global clock
        clock = self
        ref = add_weak(self, 'callback', self.clock_tick)
        self.clock = EventClock(callback=func_caller, v=ref)
        #self.clock.callbacks += self.clock_tick
        super(ClockNode, self).__init__(name)

    def start(self):
        self.clock.start()

    def stop(self):
        self.clock.stop()

    def clock_tick(self, clock, ticks):
        print 'node tick', ticks
        self.ticks = ticks


def func_caller(*args):
    global clock

    _v = args[0]
    cb = get_weak(key=_v)
    print _v, cb, clock
    return 2
