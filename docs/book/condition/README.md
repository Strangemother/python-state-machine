# Condition

A condition manages validation of routines though the network.
A condition is used to monitor change of a value on a node.
A condition maps to the running node and network dispatching
the correct responses to the network manager.

A Condition can monitor a value on a provided node. When the value
changes the condition is tried for validation.

A Condition can meet changes for:

    + A specific node
    + A name on the network

Examples of Condition use:

Use a condition as a simple boolean:

    Condition(Node, attr, value)

mapping scenario to all nodes named generic:

    Condition('generic', 'on', True)

This condition will be met `valid` when a node named 'generic' as a key `on` as `True`. This will invalidate when the condition of the node `generic` changes.

Similarly, this can be done on a single node. Rather monitoring a generic string name, a Condition can map to one or many nodes.

A single node:

    a = Node()
    Condition(a, 'on', True)


A list:

    a = Node()
    b = Node()
    Condition([a, b], 'on', True)
    Condition((a, b,), 'on', True)


Met This condition will be met when both Node `a` and `b` have an `on` state True.

A Condition can have a callback, the method will be called when the Condition is implemented.

    def light_on(node, condition, state, prev_state):
        pass

    Condition('lightbulb', 'on', True, light_on)
    Condition('lightbulb', 'on', True, valid=light_on)


+ A condition will call the valid when the condition is met.
+ A valid is called upon every condition validity called by the network

A condition can meet an exact state change:

    Condition('fruit', 'flavour', 'cherry')
    Condition('fruit', 'age', 2)


Or evaluate based on an alteration:

    Condition('fruit', 'age', POSITIVE)
    Condition('fruit', 'age', NEGATIVE)

In this case we monitor the age number up or down. This can also be applied to booleans, measured from the initial state.

    fruit.can_eat = True
    Condition('fruit', 'can_eat', POSITIVE)
    Condition('fruit', 'can_eat', NEGATIVE)

    Init    Change    Condition
    True    True      P
    True    False     N
    False   True      P
    False   False     N


