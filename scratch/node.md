# Node

A node exists on the network to as part of your applications code.

Implementing a node can be done in any method. Example cases simply extend the class. 

A node is a clean API object. It allows integration to the network. For API theory, there are a few ways a Node can work for your architecture.


## Value storage

Values can live in a transient state on the network. Assigned values are assoacited onto the network. 
Theses values can be read and changed via network alterations from other Nodes. This is defined as a *storage node*. 


    class SimpleValues(Node):
        name = 'David'
        coffee = 'black two sugars'
        age = 27


The values will not persist after the this node is removed from the network


## Reactive

A Node can react to another nodes changes on the network. When the node value alters, the listeneing node should run a method. 


    class SimpleReact(Node):
        active = False

        def simplevalue_age(self, node):
            if self.active:
                print 'Node %s changed their age' % node.name

        def reactions(self):
            return (
                Condition('SimpleValue', 'age', self.simplevalue_age)
            )


This simply reacts to a condition occuring on the network. It's very agnostic. but this can be changed to explicit conditions


## Modifier

A node can alter values of other nodes on the network. This can cause other Node reactions on a network.


    class SimpleModifier(Node):

        def __init__(self):
            self.set('SimpleReact', 'active', False)

## Validator

A node can act as a validity state by meeting a list of conditions and reacting.

    class SimpleValidator(Node):

        def get_conditions(self):
            return (
                Condition('A', 'on', True)
                Condition('B', 'on', True)
                Condition('C', 'on', True)
            )

        def valid(Node):
            print 'all conditions met'

            