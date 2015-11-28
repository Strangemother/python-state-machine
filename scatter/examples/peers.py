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
        print 'Color green', self, args, kw.get('machine')


class ColorNode(Node):
    color = 'red'


class OtherNode(Node):
    foo = 3


def run():
    example_machine = Machine('example')
    other_machine = Machine('other')
    color_node = ColorNode()
    example_machine.nodes.add(color_node)
    react_node = ReactNode()
    example_machine.nodes.add(react_node)
    other_node = OtherNode()
    other_machine.nodes.add(color_node, other_node)
    example_machine.peers.add(other_machine.bridge)
    color_node.color = 'green'
    return other_machine


def main():
    global g
    g = run()
    print g


if __name__ == '__main__':
    main()
