'''
This example shows how to implement of two nodes on a machine sharing a condition

Conditions can be coded to be agnostic or explicit

    g.nodes[0].color = 'green'
    # Node "Dave" heard "color" on Node "Cake" from red to blue
    # Node "Cake" heard "color" on Node "Cake" from red to blue

    g.nodes[1].color = 'green'
    # Node "Cake" heard "color" on Node "Dave" from red to green
    # Node "Dave" heard "color" on Node "Dave" from red to green

We use TestNode twice, each having a conditions reference to the global 'cond'
As the condition has a string reference callback, it checks if the node has
the method.

To test this, change a 'TestNode' to a 'Node'. the callback will fire once per
'color' change - on any node.
'''
from scatter import Machine, Node, Condition


class BNode(Node):

    _conditions = (
            Condition('color', Condition.CHANGED, 'color_changed', node='BNode'),
        )

    def color_changed(self, node, key, new_val, old_val, condition, valids):
        print 'B heard A color change', new_val


class ANode(Node):
    _conditions = (
            Condition('color', Condition.CHANGED, 'color_changed', node='ANode'),
        )

    def color_changed(self, node, key, new_val, old_val, condition, valids):
        print 'A Heard B color change', new_val


class CNode(Node):
    _conditions = (
            Condition('color', Condition.CHANGED, 'color_changed', node='ANode'),
        )

    def color_changed(self, node, key, new_val, old_val, condition, valids):
        print 'C Heard color change on', node


def run():
    ma = Machine('example')
    a = ANode()
    b = BNode()
    c = CNode()
    ma.nodes.add(a, b, c)
    a.color = 'red'
    b.color = 'blue'
    return ma


def main():
    global g
    g = run()


if __name__ == '__main__':
    main()
