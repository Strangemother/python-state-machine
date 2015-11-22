import sys
import subprocess
import random
import time
import threading
from multiprocessing import Process, Queue
from axel import Event
from weak import add_weak, get_weak


STOP = 'STOP'


class AsyncClock(Process):

    def __init__(self, queue, interval=1, cb=None):

        super(AsyncClock, self).__init__()
        self.ticks = 0
        self._queue = queue
        self.running = False
        self.interval = interval
        self._last = None
        self.cb = cb

    def start(self):
        self.running = True
        super(AsyncClock, self).start()

    def run(self):
        stop_flag = False

        while self.running is True and (stop_flag is False):
            self.ticks += 1 * self.interval
            self.set_ticks()
            time.sleep(self.interval)
            stop_flag = self.get_q() == STOP

        self.set_ticks()
        self._queue.close()

    def get_q(self):
        res = self._last
        if hasattr(self, '_queue') is False:
            return res
        while not self._queue.empty():
            res = self._queue.get_nowait()
            print 'q',res
        self._last = res
        return res

    def set_ticks(self):
        #with self._queue.mutex:
        #    self._queue.queue.clear()
        self._queue.put_nowait(self.ticks)

        self.callback(self.ticks)

    def callback(self, ticks):

        if self.cb:
            res = self.cb(self.ticks)

            if isinstance(res[0], tuple) and res[0][0] == False:
                self.callback_error(res[0][2], res[0][1])

    def callback_error(self, sender, error):
        print 'Error from:', sender
        raise error


class Clock(object):

    def __init__(self, interval=1):
        self.interval = interval
        self._last = 0

        self.q, self.thr = self.create_thread(self.interval)

    def tick(self, ticks):
        '''
        The callback provided to the AsyncClock. When called; the self will
        be AsyncClock not 'Clock' - as it's callbacked by the other process
        '''
        print 'clock', ticks

    def cbs(self):
        pass

    def create_thread(self, i):
        _q = Queue()
        return (_q, AsyncClock(_q, i, self.tick))

    def start(self):
        if hasattr(self, 'thr') is False:
            self.q, self.thr = self.create_thread(self.interval)

        self.thr.start()

    def stop(self):
        self.thr.running = False
        self.put_q(STOP)
        self.thr.join()
        self.get_q()
        # self.thr.terminate()
        # self.interval = self._last


    def reset(self):
        self._last = 0

    def get_q(self):
        res = self._last
        if hasattr(self, 'q') is False:
            return res
        while not self.q.empty():
            line = self.q.get()
            res = line
        self._last = res
        return res

    def put_q(self,v):
        self.q.put_nowait(v)

    def get_count(self):
        self.get_q()
        return self._last

    count = property(get_count)

import threading
clock_weaks = None
some_rlock = threading.RLock()

class EventClock(Clock):
    '''
    An EventClock alters the tick() callback passed to the AsyncClock. Rather
    than a python def self.ticks is an axel.Event. The event calls 'on_click'.
    As the signature of the event caller self.tick is the same as a method,
    no changes to the AsyncClock are required.

    When on_tick is called the sender and ticks are provided as arguments.
    You'll notice the scope of the method 'on_click' is not the AsyncClock but
    the relative class EventClock.
    '''

    def __init__(self, interval=1, callback=None, v=None):
        super(EventClock, self).__init__(interval)
        self.callbacks = Event(self)
        self.tick = Event(self)
        self.callbacks += self.on_callback
        self.tick += self.on_tick
        self.tick += self.callbacks
        if callback is not None:
            self.callback = callback
            self.v = v
            # clock_weaks = callback
            # self.cb_ref = add_weak(self, 'callback', callback)
            # print 'Ref:', self.cb_ref, callback


    def on_tick(self, sender, ticks):
        res = self.callbacks(sender, ticks)
        if isinstance(res[0], tuple) and res[0][0] is False:
            print res[0]

        return ('on_tick', ticks)

    def on_callback(self, sender, *args):
        # self.callbacks(args[0])
        # cb = get_weak(key=self.cb_ref)
        # print 'weak', self.cb_ref, clock_weaks
        cb = self.callback
        v = self.v
        if cb is not None:
            # print 'manager', cb
            cb(v)
            # print 'ret', self.count, '\n'
        return ('on_callback', self.count)
