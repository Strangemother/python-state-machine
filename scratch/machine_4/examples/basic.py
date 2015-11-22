from machine import Machine
from node import Node
from conditions import Condition


class TestNode(Node):
    color = 'red'
    age = 22
    food = 'cherry'
    bar = 2

    def heard_food(self, node, value, field):
        print 'I HEARD THAT'

    def conditions(self):
        C = Condition
        return (
            C('TestReactNode', 'heard_food', True, self.heard_food, name='test_heard_food'),
        )

class TestReactNode(Node):
    heard_food = False

    def node_age(self, node, value, field):
        print '! ', self.get_name(), 'AGE is 3'

    def node_age_changed(self, node, value, field):
        print '! ', self.get_name(), 'CHANGE', field, value
        # print 'Condition', node, field, value

    def node_food_changed(self, node, value, field):
        print "> ", self.get_name(), 'FOOD', field, value
        self.heard_food = True

    def conditions(self):
        C = Condition
        return (
            C('TestNode', 'age', 3, self.node_age, name='react_age_3'),
            C('TestNode', 'age', C.CHANGED, self.node_age_changed, name='react_age_change'),
            C('TestNode', 'food', C.CHANGED, self.node_food_changed, name='react_food_change')
        )


def run():
    print 'machine example'
    ma = Machine('example')
    n = TestNode()
    n2 = TestReactNode()
    ma.add(n)
    ma.add(n2)
    print 'change age on first node'
    n.age = 7
    n.age = 3
    n.age += 3
    n.color = 'green'
    n.food = 'Noodles!'
    print 'done'
    return ma

def main():
    return run()


if __name__ == '__main__':
    main()
