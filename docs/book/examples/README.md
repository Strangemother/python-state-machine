# Examples

Built into scatter are examples to help you get started. Each example shows a certain aspect of scatter.

You can use examples in your code or simply run them and play with the code. You can find all examples in `scatter.examples`

to view a list of available examples bundled with the source and how they are ran:

```python
$ python -m scatter.examples
'''
The example files show basic operations and setups for scatter Nodes, Conditions
and Managers. Running an example

$ python -m scatter.examples.basic

$ python
>>> from scatter.examples import basic
>>> machine = basic.run()

--------------------------------------------------------------------------------

A List of provided examples:

basic ...
'''
```

### Running

There are a few ways to run the examples. All examples are written in the same way. Much of this is basic python setup so they're easy to follow:

If you have `scatter` installed in your environment through your standard `pip` location or within a `virtualenv`, you can pip straight to a file with your code.
In this case we presume the main `scatter` folder is local.

    $ python ./scatter/examples/basic.py

You can run the examples as a module

    $ python -m scatter.examples.basic

To be clever, add the python `-i` flag. This will allow interation after the main source is complete. Each example file applies `global g`, storing the `Machine` or other _global_  reference the example file ran.

```python
$ python -im scatter.examples.basic
>>> repr(g)
'<machine.Machine:Machine("example")>'
>>> print g
'Machine "example"'
>>>
```

You can run and continue to use an example file.

---

An example can be imported and ran like any code:

```python
>>> from scatter.examples import basic
>>> machine = basic.run()
```


Importing code from an example is performed in the normal method:

```python
from scatter.examples.basic import TestNode

class MyNode(TestNode):
    age = 6

node = MyNode()
print node.color
# 'red'
print node.age
# 6
```

---

This is all pretty boring stuff, but ensure to use the examples like boilerplate code.
