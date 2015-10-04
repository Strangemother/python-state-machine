from scatter import Machine, Node, Condition

class Test(Node):
    age = 4

    _conditions = (
            Condition('Test', 'age', 5),
        )

m = Machine()
n = Test()
m.nodes.add(n)
