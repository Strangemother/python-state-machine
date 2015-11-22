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


cond = Condition('color', Condition.CHANGED, 'color_changed')


class TestNode(Node):
    color = 'red'

    _conditions = (
            cond,
        )

    def color_changed(self, node, key, new_val, old_val, condition, valids):
        '''
        color changed condition handler. Will fire when any node.color alters.
        '''
        s = '{0} heard "{1}" on {2} from {3} to {4}'
        sargs = [self, key, node, old_val, new_val]
        print s.format(*sargs)


def run():
    ma = Machine('example')
    n = TestNode('Cake')
    n2 = TestNode('Dave')
    ma.nodes.add(n, n2)
    n.color = 'blue'
    return ma


def main():
    global g
    g = run()


if __name__ == '__main__':
    main()
