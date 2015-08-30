from machine import Machine
import machine
from address import Address
from node import Node
from conditions import Condition


class TestNode(Node):
    color = 'red'

def run():
    ma = Machine('example')
    m1 = Machine('foo')
    m2 = Machine('bar')
    n = TestNode()
    ma.add(n)

    a = Address()._make(machine=ma, nodes=[n])
    print '+ 1 Address:', str(a)
    # a = Address()._make(nodes=[n])
    # print '+ 2 Address:', str(a)
    # a = Address()._make(machine=ma, machines=[m1, m2], nodes=[n])
    # print '+ 3 Address:', str(a)
    # a = Address()._make(machine=ma, machines=[m1, m2])
    # print '+ 4 Address:', str(a)
    return a

def main():
    return run()


if __name__ == '__main__':
    main()
