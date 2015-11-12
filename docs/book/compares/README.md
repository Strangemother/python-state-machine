# Compares

a `Compare` class helps evaulate a pair of values to determine a `True` or `False` based upon the comparison defined.

The `Condition` will use a `Compare` instance to determine alterations of a `Node` attribute. A `Compare` class doesn't need special setup:

```python
>>> from scatter.compares import Exact
>>> compare = Exact()
>>> compare.match(1,2)
False
>>> compare.match(2,2)
True
>>> compare.match('apples', 'apples')
True
```

It's not very exciting but they allow a condition to easily define a transition of a value in a direction.

### Compare Example

A `Positive` compare returns true if value `A` is greater than `B`. The `Negative` performs the opposite. `Changed` simply determines a difference between `A` and `B`

```python
>>> from scatter.compares import Positive
>>> positive = Positive()
>>> positive.match(1,0)
True
>>> positive.match(40,50)
False
```

```python
>>> from scatter.compares import Changed
>>> changed = Changed()
>>> changed.match(3,3)
False
>>> changed.match(3,6)
True
```

#### Using Compares in Conditions

Some interesting Compare classes are built-in. They help with basic reactions to nodes within a machine.

Let's look at a basic `Condition` setup:

```python
from scatter import Node, Condition

def vf(node, key, new_val, old_val, condition, valids):
    print 'Key %s created on %s' % (node.get_name(), key)

n = Node()
c = Condition(foo=Condition.CREATED, valid=vf)
n._conditions = (c, )
```

This states when the attribute `foo` is created on our Node `n` the valid function `vf` is called. The `CREATED` Compare will only fire when a value changes from `None` to _not_ `None`

Changing `foo` will trigger the callback to fire:
```python
>>> n.foo=1
# Key Node created on foo
```
----

The exact setup can be done in a class structure:
```python
from scatter import Machine, Node, Condition
from scatter.compares.const import Const as const

class Test(Node):
    age = 4

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
