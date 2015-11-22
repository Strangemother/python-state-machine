from machine import Machine
from node import Node
from conditions import Condition as C
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
    )

    def a_one_changed(self, node, value, field):
        print 'B Said: A has changed', value


class CC(Node):

    _conditions = (
        C('A', 'one', C.CHANGED, 'a_one_changed'),
    )

    def a_one_changed(self, node, value, field):
        print 'C Said: A has changed', value


class D(Node):

    _conditions = (
        C('A', 'one', C.CHANGED, 'a_one_changed'),
    )

    def a_one_changed(self, node, value, field):
        print 'D Said: A has changed', value


class E(Node):

    _conditions = (
        C('A', 'one', C.CHANGED, 'a_one_changed'),
    )

    def a_one_changed(self, node, value, field):
        print 'E Said: A has changed', value


def run():
    print 'running simple machine'
    m = Machine()
    a = A()
    b = B()
    c = CC()
    d = D()
    e = E()
    m.add(a)
    m.add(b)
    m.add(c)
    m.add(d)
    m.add(e)

    # print 'm.conditions'
    # pprint(m.conditions)
    # print 'm.condition_keys'
    # pprint(m.condition_keys)
    # print 'm.condition_nodes'
    # pprint(m.condition_nodes)

    print 'perform a.one += 4'
    a.one += 4
    return a


def main():
    return run()


if __name__ == '__main__':
    main()
