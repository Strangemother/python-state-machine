from machine import Machine
from node import Node
from conditions import Condition


class TestNode(Node):
    color = 'red'
    age = 22
    food = 'cherry'
    bar = 2


class TestReactNode(Node):

    def testnode_age(self, node, value, field):
        print self.get_name(), 'A condition has been met.'
        print 'Condition', node, field, value

    def conditions(self):
        from conditions import Condition

        return (
            Condition('TestNode', 'age', 3, self.testnode_age),
        )


class Runner(object):

    def run(self, cmd, *args, **kwargs):

        m = getattr(self, cmd)
        if m is not None:
            return m(*args, **kwargs)

    def ran(self):
        self._ran = True
        return True


    def hello(self):
        s = 'Hello?.. Are you there?.. Can you hear me?..'
        return s

    def machine(self):
        print 'machine example'
        ma = Machine('example')
        n = TestNode()
        n2 = TestReactNode()
        ma.add(n)
        ma.add(n2)
        print 'change age on first node'
        n.age = 3
        print 'done'

        return ma
