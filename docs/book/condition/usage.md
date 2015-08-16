# Condition Usage

A condition is simple enough, it has some values of which are met from the parent call.

the `Condition()` has three base values.

+ Item to watch

 first arg is the item to monitor on the network. This is a name or a node; something to monitor.

 ```python
c = Condition('TestNode')
c.watch
'TestNode'
```

+ Item field

 The field of the monitored object as argument 2.

 ```python
c = Condition('TestNode', 'age')
c.field
'age'
```

+ Item target

 The target is the value to meet when a condition is met by the first two arguments. This can be an exact match, or denote a change in a direction.

 In this example. We match the age in serveral methods:

 ```python
# exact match
c = Condition('TestNode', 'age', 5)
# match value in a positive direction
c = Condition('TestNode', 'age', POSITIVE)
# match negative direction
c = Condition('TestNode', 'age', NEGATIVE)
# match a change has occured.
c = Condition('TestNode', 'age', CHANGED)
c.target
'CHANGED'
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

