# Callbacks

When a condition validates it can have a callback. Every time your condition is run and validates `True` the callback will fire


```python
from scatter import Node, Condition

def foo_one(node, key, new_val, old_val, condition, valids):
    print 'foo is one'
    return True

c = Condition('foo', 1, foo_one)
n = Node()
n._conditions = (c, )
n.foo = 1
# 'foo is one'
```


### Machine implement

A condition is provided to a node. This node will react to the condition met. Condition strings are maintained by the Machine. events from Nodes within the machine are captured by the machine. The event string is checked against all the conditions contained with every node.

When the machine meets a condition matching the event (by simple string pattern) the condition is validated.

If the condition validates it respondes by calling your callback.

```python
from conditions import Condition

class TestReactNode(Node):

    def testnode_age(self):
        print 'test node age has changed'

    def conditions(self):
        return (
            Condition('OtherTestNode', 'age', 3, self.testnode_age),
        )
```

This example shows when the value `age` on `OtherTestNode` is `3`, our callback will print it's response. We add our `TestReactNode` to the Machine in order to make it a reality.

```python
m = Machine()
m.add(TestReactNode())
```


Adding a test node to make is happen.

```python
class OtherTestNode(Node):
    age = 22

n = OtherTestNode()
m.add(n)
n.age = 5
# TestReactNode prints
'test node age has changed'
```

That's pretty easy. Simply extend this model to implement a massive reactive chain.
