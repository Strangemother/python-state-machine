'''
This example shows how to implement a node to a machine.
The ColorNode contains a value "color".

The condition will react when 'color' is changed on the node.

    g.nodes[0].color = 'green'
    # 'Color changed from blue to green'
'''
from scatter import Machine, Node, Condition


class ColorNode(Node):
    color = 'red'

    _conditions = (
            Condition('color', Condition.CHANGED, 'color_changed'),
        )

    def color_changed(self, node, key, new_val, old_val, condition, valids):
        print 'Color changed from {0} to {1}'.format(old_val, new_val)


def run():
    ma = Machine('example')
    n = ColorNode()
    ma.nodes.add(n)
    n.color = 'blue'
    return ma


def main():
    global g
    g = run()


if __name__ == '__main__':
    main()
