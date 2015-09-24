from machine import Machine
from node import Node
from conditions import Condition


class TestNode(Node):
    alpha = 1
    beta = 2
    charlie = 3
    delta = 4
    echo = 5

    def heard_delta(self, node, value, field):
        print 'I heard TestReactNode saw my delta change'

    def conditions(self):
        C = Condition
        return (
            C('TestReactNode', 'heard_delta', True, self.heard_delta),
        )

class TestReactNode(Node):
    heard_delta = False

    def alpha3(self, node, value, field):
        print 'alpha is 3'

    def charlie_changed(self, node, value, field):
        print '! ', self.get_name(), 'CHANGE', field, value
        # print 'Condition', node, field, value

    def delta_changed(self, node, value, field):
        print 'delta changed', value
        self.heard_delta = True

    def conditions(self):
        C = Condition
        return (
            C('TestNode', 'alpha', 3, self.alpha3),
            C('TestNode', 'charlie', C.CHANGED, self.charlie_changed),
            C('TestNode', 'delta', C.CHANGED, self.delta_changed)
        )


def run():
    print 'machine example'
    ma = Machine('example')
    n = TestNode()
    n2 = TestReactNode()
    ma.nodes.add(n)
    ma.nodes.add(n2)
    n.alpha = 3
    return ma

def main():
    return run()


if __name__ == '__main__':
    main()
