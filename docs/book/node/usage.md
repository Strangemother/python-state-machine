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

---

due to the method of communication build into a machine
