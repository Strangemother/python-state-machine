from machine import Machine
import machine
from proxy import ProxyNode
from address import Address
from node import Node
from conditions import Condition


class TestNode(Node):
    color = 'red'

class OtherNode(Node):
    color = 'Green'

class Prox(ProxyNode):
    color = 'red'

def run():
    ma = Machine('example')
    m1 = Machine('foo')
    m2 = Machine('bar')
    n = TestNode()
    n2 = OtherNode()
    pr = Prox()

    a = Address('example.TestNode')
    pr.address = a

    print '---add machines---'
    ma.add(n, n2, pr)
    ma.add_peer('PYRO:obj_47120b94fb6347e89c1ed65024e2061b@localhost:56894')
    ma.add_peer('PYRO:obj_fd447709e96f4ce4a20cfc6c6b3b5dc9@localhost:41106')
    return ma

def main():
    return run()


if __name__ == '__main__':
    main()
