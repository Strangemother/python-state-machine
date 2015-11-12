# Usage

A node is the entry point to the network and it's changes. By changing a nodes value, the machine will detect, distribute and react to the change.


```python
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
```

This node has some attributes `alpha` through `echo`. When these values change condtions can be met.

The `conditions` denote reactions to occur when the network value is altered. when the Condtion is met the handler function is called.
In this example when some node `TestReactNode` changes its field `heard_delta` to `True` the method `self.heard_delta` is called.

When you want to get your node to work - at it to a `Machine` - this churns out changes on a network of nodes.

```python
m = Machine()
m.add(TestNode())
```

That's as complex as it gets! write your code and perform changes on the node.

## Getting Started

A node can exist outside of a `Machine` and network. Essentially a node is an empty object - Each key value alteration is dispatched through an event layer.

You can see what happens under-the-hood:

```python
>>> import scatter
>>> n=scatter.Node()
# x   Node "Node" Error on _event existence for set
# set _event_handlers <axel.axel.Event object at 0x0000000002C1C278>
# dispatch set _name
# set _name None
>>> n.foo = 3
# dispatch set foo
# set foo 3
>>> n.foo = 2
# dispatch set foo
# set foo 2
>>> n.foo = 2
```

You can name a node as it's first argument

```python
>>> nn = scatter.Node('foo')
# x   Node "Node" Error on _event existence for set
# set _event_handlers <axel.axel.Event object at 0x0000000002C884E0>
# dispatch set _name
# set _name foo
```

## Implementation

Because a node is designed to be the extendable part of the API, it has a small set methods:

Here is a list of attribute names in a node. Unless you `super` override these methods, you'll break the `Node` instance.

```python
['_build_event',
'_conditions',
'_dispatch',
'_event_handlers',
'_name',
'conditions',
'event_result',
'get',
'get_name',
'set']
```

#### name & and get_name()

The `get_name` method will return the string name of the node. If no name was provided when the node was instansiated, The class name is returned.

```python
>>> n = scatter.Node()
>>> n.get_name()
'Node'
```

Passing a name when creating a node will change the return value
```python
>>> n = scatter.Node('foo')
>>> n.get_name()
'foo'
>>> n.name
# None
>>> n._name
'foo'
```

The `name` key of a node is a reserved word for a node. This may be assigned by an attached machine. The instance name is not the 'name'.

You can use the name to define a special word for your network. Before you edit this name attribute, the chapter on `Machine` will help.

#### set(`key, value`)

The `set` method writes an attribute and it's value to the node. It works like any given _set_ method. When you overload your node with a new attribute, the set method is used.

```python
>>> n.set('bar', 'zales')
# dispatch set bar
# set bar zales
>>> n.bar
'zales'
>>> n.get('bar')
'zales'
```

The `Node` class overrides `mixins.GetSetMixin.set` calling `self._dispatch('set', k,v)` before calling the super `set` method from the mixin.

The _dispatch method perpetuates the set attribute through an attached machine.

#### get(`key`)

```python

>>> n.get('bar')
'zales'
>>> n.get('foo')
2
>>> n.get('fo')
# None
>>>
```

If an attribute is not defined on a node `None` is returned, no error is raised. the `Node` class recieves this method from `mixins.GetSetMixin.get`.

#### _dispatch(`name, *args, **kw`)

The dispatch comment wil send data through the `_event_handlers`. The result of each event handler is given to `event_result()`

The `set` method will use the `_dispatch` method when an attribute is applied to the `Node`.

```python
>>> n = scatter.Node()
>>> n._dispatch('set', 'key', 'value')
# dispatch set key
```

is method is applied with the `mixins.EvenMixin`

#### conditions()

A `Node` can be provided with a list of conditions. when an attribute is altered on a `Node` the conditions tuple is iterated. If a condition is met the handler is called.

The `conditions()` method returns a `tuple` of `_conditions`. When creating a node of which has a set of conditions you should add them to the `_conditions`.


```python

from scatter import Node, Condition

class TestNode(Node):

    _conditions = (
            Condition('OtherTestNode', 'age', 3, 'age_change'),
        )

    def age_change(self):
        print 'test node age has changed'

```

If a condition requires a callback, you can return a tuple from the method:

```python
class TestNode(Node):

    def testnode_age(self):
        print 'test node age has changed'

    def conditions(self):
        return (
            Condition('OtherTestNode', 'age', 3, self.testnode_age),
        )
```

