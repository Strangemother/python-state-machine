from scatter import Machine, Node, Condition
from scatter.compares.const import Const as const


def vf(node, key, new_val, old_val, condition, valids):
    print 'node', node, 'validated', valids

def foo_one(node, key, new_val, old_val, condition, valids):
    print '!  foo is one'
    return True
    # node.set('dibble', 1)

m = Machine()
n = Node()
# c = scatter.Condition(value=Condition.POSITIVE)
c = Condition('foo', 1, foo_one, name='floating', node='Test')
c2 = Condition(foo=3, bar='fiz', valid=vf)
n._conditions = (c, c2, )

m.nodes.add(n)

n.bar = 'fiz'


class Test(Node):
    age = 4

    _conditions = (
            Condition('age', 5),
            Condition('foo', 1, valid='node_foo_1'),
            Condition('baz', const.CREATED, valid='baz_created'),
        )

    def node_foo_1(self, *args, **kw):
        print '!  TestNode node foo 1'
        return True

    def baz_created(self, node, key, new_val, *args, **kw):
        print '!  Baz created on', node.get_name()
        return True

m2 = Machine('Other')
n2 = Test()
m2.nodes.add(n, n2)

def v3f(node, key, new_val, old_val, condition, valids):
    print 'Key %s created on %s' % (node.get_name(), key)

n3 = Node()
c3 = Condition(foo=Condition.CREATED, valid=v3f)
n3._conditions = (c3, )
