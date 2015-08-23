from machine import Machine
from node import Node
from conditions import Condition as C
from pprint import pprint
import threading

from threading import Timer,Thread,Event
import random

class perpetualTimer():

    def __init__(self,t,hFunction, scope=None):
        self.t=t
        self.hFunction = hFunction
        self.scope = scope
        self.thread = Timer(self.t,self.handle_function)

    def handle_function(self):
        if self.scope is not None:
            self.hFunction(self.scope)
        else:
            self.hFunction()

        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

class Hand(Node):
    value = 0
    threshold = 4

    def tick(self):
        if self.value > self.threshold + 1:
            # print 'clock reset over value.'
            self.value = 0
        print 'Tick ', self.__class__.__name__,':', self.value


class Second(Hand):

    def tick(self):
        self.value += 1 # random.randint(1,100)
        super(Second, self).tick()


class Minute(Hand):

    monitor = 'Second'

    def conditions(self):
        return (
            C(self.monitor, 'value', C.CHANGED, 'tock'),
        )

    def tock(self, node, value, field):

        if value > self.threshold:
            self.value += 1

        print 'Tock ', self.__class__.__name__, ':', self.value


class Hour(Minute):
    monitor = 'Minute'


class Clock(Machine):
    name = 'clock'

    def run(self):
        t = perpetualTimer(1, self.timer_tick)
        t.start()

    def timer_tick(self):
        sn = self.nodes
        for n in sn:
            n.tick()


def run():
    clock = Clock()
    ss = Second()
    hh = Hour()
    nodes = [ss, Minute(), hh]
    clock.add(*nodes)
    print hh.conditions()
    clock.run()
    # clock.loop()
