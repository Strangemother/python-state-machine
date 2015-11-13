'''
This example shows how to implement a node to a machine.
The TestNode contains a value "color".
'''
from scatter import Machine, Node, Condition


class TestNode(Node):
    color = 'red'

def run():
    ma = Machine('example')
    n = TestNode()
    ma.nodes.add(n)
    return ma

def main():
    global g
    g = run()


if __name__ == '__main__':
    main()
