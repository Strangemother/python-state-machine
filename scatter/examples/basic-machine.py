'''
This example shows how to implement a node to a machine.
The ColorNode contains a value "color".
'''
from scatter import Machine, Condition, Node


class ReactNode(Node):

    _conditions = (
            Condition('color', 'green', 'color_green'),
        )

    def color_green(self, *args, **kw):
        print 'Color green'


class ColorNode(Node):
    color = 'red'


def run():
    ma = Machine('example')
    n = ColorNode()
    n2 = ReactNode()
    ma.nodes.add(n, n2)
    n.color = 'green'
    return ma


def main():
    global g
    g = run()
    print g


if __name__ == '__main__':
    main()
