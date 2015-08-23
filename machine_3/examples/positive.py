from machine import Machine
from node import Node
from conditions import Condition as C
from tools import color_print as cl

from pprint import pprint


class A(Node):
    '''
    A node simply exists to
    store your variables
    '''
    one = 1


class B(Node):

    _conditions = (
        C('A', 'one', C.CHANGED, 'a_one_changed'),
        C('A', 'one', C.POSITIVE, 'a_one_negative'),
        C('A', 'one', C.NEGATIVE, 'a_one_positive'),
        C('A', 'two', C.CHANGED, 'a_two_changed'),
    )

    def a_one_changed(self, node, value, field):
        cl('white','B Said: A will change to', value )# , 'from', node.one)

    def a_two_changed(self, node, value, field):
        cl('white','B Said: A.two will change to', value )# , 'from', node.one)

    def a_one_negative(self, node, value, field):
        cl('white','B Said: A has NEGATIVE', value)

    def a_one_positive(self, node, value, field):
        cl('white','B Said: A has POSITIVE', value)


def run():
    cl('white','running direction direction')
    m = Machine()
    a= A()
    nodes = [a, B()]
    m.add(*nodes)
    a.one += 1
    a.one -= 1
    a.one = 4


def main():
    return run()


if __name__ == '__main__':
    main()
