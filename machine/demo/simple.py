from core import Machine, Node
from core.nodes import Walker
from core.conditions import Condition as C
from pprint import pprint


class House(Node):
    people = 2


class LivingRoom(Node):
    lights = 'auto'
    people = 0

    def get_conditions(self):
        return [
            C('Lightbulb', 'installed', False)
        ]




class Lightbulb(Node):
    on = False
    installed = True

    _conditions = (
        C('LivingRoom', 'lights', 'auto'),
        C('LivingRoom', 'people', 1),
    )

    def valid(self):
        print 'Light can be turned on.'
        # self.set('on', True)


def run():
    m = Machine('My Home')
    m.start([ House(), LivingRoom() ])
    m.activate_node( Lightbulb() )

    lb = m.nodes.get('Lightbulb')

    # w = Walker(lb[0])
    # t = w.walk(machine=m)
    # pprint(t)
    #import pdb; pdb.set_trace()

