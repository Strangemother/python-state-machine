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


def run():
    print 'running simple machine'
    m = Machine()
    m.add_peer('PYRO:obj_d49b952840174542be460c635eec8436@localhost:55090')
    a = A()
    m.add(a)

    print 'perform a.one += 4'
    a.one += 4
    return m


def main():
    return run()


if __name__ == '__main__':
    main()
