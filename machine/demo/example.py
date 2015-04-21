from core import Machine, Node
from core.conditions import Condition as C
from pprint import pprint

class A(Node):
    on = False
    foo = 'Wibble'

    def get_conditions(self):
        conds = [
            # No state provided defaults State.CHANGED
            C('B', 'on', True),

            # Also condition should be set False
            C('X', 'on', False),
        ]

        return conds


class B(Node):
    on = False

    def get_conditions(self):
        '''
        Returns the conditions to be set for the node.
        When this state is completely true, the Node is
        completed and a state is performed.

        In this case. A.foo = 'bar' would validate this
        condition, validating this Node.
        '''
        return [
            C('A', 'foo', 'bar')
        ]


class D(Node):
    on = False


class E(Node):
    on = False


class X(Node):
    on = False

    def cond_B_on_True(self, node):
        '''
        This node condition is set to
        change. B<C:0> should react. B should be
        valid.
        '''

        self.log('callback X cond_B_on_True', node)

        # a = self.nodes.get('A')
        # a.foo = 'bar'

    def get_conditions(self):
        return [
            C('B', 'on', True, callback=self.cond_B_on_True),
            C('F', 'on', True)
        ]


class G(Node):
    on = False

    def get_conditions(self):
        '''
        G Simply reacts to F on False.
        As default is this state, the G
        should activate on F expose.
        '''
        return [
            C('F', 'on', False)
        ]


class F(Node):
    on = False


class H(Node):
    on = True
    _conditions = (
        C('A', 'on', True),
        C('B', 'on', True),
        C('D', 'on', True),
        C('E', 'on', True),
        C('F', 'on', True),
        C('G', 'on', True),
        # C('H', 'on', True),
    )

def expose(*args, **kw):
    print 'got expose', kw.get('node')

def valid(*args, **kw):
    print 'Valid: ', kw.get('node')

def run():
    machine = Machine('example')
    nodes = [A(),B(), X(), G()]
    machine.events.listen('expose', expose)
    machine.events.listen('valid', valid)
    machine.start(nodes)

    # B:True
    #   A<C:0>
    #   X<C:0> A.foo = 'bar'
    #       B<C:0> +
    b = machine.nodes.get('B')

    b.set('on',True)
    b = machine.nodes.get('B')
    b.set('red','dwarf')

    machine.activate_node( F() )
    f = machine.nodes.get('F')
    f.set('on', True)

    x2 = machine.activate_node( X() )
    x2.set('on',True)

    machine.activate_node( D() )
    h = machine.activate_node( H() )
    machine.activate_node( E() )
    machine.activate_node( G() )

    # [<demo.example.A object at 0xb7181bac>, <demo.example.B object at 0xb7181c4c>, <demo.example.X object at 0xb7181d4c>]
    print 'register.nodes'
    pprint(machine.register.nodes)
    # {'A': {}, 'X': {}, 'B': {}}
    print 'register.conditions'

    pprint( machine.register.conditions )
    # {'B.on:changed': ['A', 'X'], 'A.foo:bar': ['B'], 'X.on:False': ['A']}

    import pdb; pdb.set_trace()
    # dipatch change


