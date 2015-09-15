from machine import Machine
from node import Node
from conditions import Condition as C
from pprint import pprint
import threading

from time import sleep
import random


class Tick(Node):
    value = 0

    def _start(self):
        run = True
        while run:
            try:
                sleep(1)
                self.tick()
            except KeyboardInterrupt as e:
                run = False
                print 'stop'

    def tick(self):
        self.value += 1
        print 'Tick ', self.__class__.__name__,':', self.value


class Clock(Machine):
    name = 'clock'

    def timer_tick(self):
        sn = self.nodes
        for n in sn:
            n.tick()


def run():
    clock = Clock()
    n = Tick()
    nodes = [n]
    clock.add(*nodes)
    clock.add_peer('PYRO:obj_4be193a9e0a243b6a8a61a215c648940@localhost:39199')
    n._start()
    return clock
