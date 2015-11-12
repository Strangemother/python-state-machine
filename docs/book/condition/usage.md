# Using a Condition

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

## Basic Usage

A condition is essentially an `if` statement exising in its own logic state. You can use a `Condition` and its without a `Node` or `Machine`:

```python
>>> import scatter
>>> c = scatter.Condition()
>>> c.match(1,1)
# Match conditions 1 1
True
>>> c.match(1,2)
# Match conditions 1 2
False
```

More advanced Conditions may match more than an exact `1` and `1`. You can provide a `Condition` with a `value` to match.

A Condition implements an underlying `Compare` class. Lets quickly look at one:

```python
>>> from scatter.conditions import Positive
>>> p=Positive()
>>> p.match(1,0)
True
```

Now lets use that basic `Compare` in a `Condition`:

```python
>>> from scatter import Condition, Node
>>> c = Condition(attr='foo', value=Condition.POSITIVE)
>>> n = Node()
>>> n._conditions = (c,)
```

Changing foo from a smaller value to a greater value would `_valid` this node.

```python
n.foo = 1
n._valid == True
# True
```

Now we understand how a `Compare` works, we can use them in our condition


## Node Usage

We can set up a condition in a `Node` with minimal effort. In this example we set the condition to match a value:

```python
from scatter import Node, Condition
n = Node()
c = Condition('foo', 1)
n._conditions = (c,)
```

When the node attribute `foo` is `1` the condition will fire. Nothing special will happen but you can validate a node

```python
# Extended from above
n.foo = 1
n._valid
# True
```

A more useful implementation of a Condition allows callbacks on certain events.


#### Callback: Functional

This example shows when the attribute `foo` is created on our Node `n`, the function `foo_created` is called. The `Condition.CREATED` comparison will only fire when a value changes from `None` to _not_ None:

```python
from scatter import Node, Condition

def foo_created(node, key, new_val, old_val, condition, valids):
    print 'Key %s created on %s' % (node.get_name(), key)

n = Node()
c = Condition(foo=Condition.CREATED, valid=foo_created)
n._conditions = (c, )
```


Changing `foo` will trigger the callback to fire:
```python
>>> n.foo=1
# Key Node created on foo
```

#### Callback: Class

A basic `Node` is designed to be very flexible. The conditions can run with context of a Node.

The exact setup shown above can be done in a class structure:
```python
from scatter import Machine, Node, Condition
from scatter.compares.const import Const as const

class Test(Node):
    _conditions = (
            Condition('foo', const.CREATED, valid='foo_created'),
        )

    def foo_created(self, node, key, new_val, *args, **kw):
        print 'Foo created on', node.get_name()
        return True
```

You would run this:

```python
n = Test()
n.foo = 1
# Key Node created on foo
```
