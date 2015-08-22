from base import Base
from nodes import Nodes, Node
from tools import random_string
from events import Events
import events
import inspect


class Machine(Base):
    '''
    The machine connects the nodes and manages the addition
    and removal of nodes to the network.
    '''
    def __init__(self, name=None):
       pass

    def __str__(self):
        return '%s "%s"' % (self.__class__.__name__, self.name, )
