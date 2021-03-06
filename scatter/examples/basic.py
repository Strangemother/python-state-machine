'''
This example shows how to implement a node to a machine.
The ColorNode contains a value "color".
'''
from scatter import Machine, Node


class ColorNode(Node):
    color = 'red'


def run():
    ma = Machine('example')
    n = ColorNode()
    ma.nodes.add(n)
    return ma


def main():
    global g
    g = run()
    print g


if __name__ == '__main__':
    main()
