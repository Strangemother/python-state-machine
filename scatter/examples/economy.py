from scatter import Machine, Node, Condition

step_cond = Condition('step_val', Condition.CHANGED, 'step_changed')

class PersonNode(Node):

    _conditions = (
        Condition('color', Condition.CHANGED, 'color_changed', node='person'),
        Condition('color', Condition.CHANGED, 'color_changed', node='person'),
        step_cond,
        # Condition('step_val', Condition.CHANGED, 'calendar_step_val_changed', node='calendar'),
    )

    def color_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        print '{} heard {} {}'.format(self.index, condition, new_val)

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        '''
        A calendar has stepped time to a value specified.
        '''
        print '{} heard {} {}'.format(self.index, condition, new_val)



class Person(PersonNode):
    age = 20
    step_val = 0

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        self.step_life(new_val)

    def step_life(self, val):
        if self.index == 40:
            print 'person(40) step life', self.age + self.step_val

class CalendarNode(Node):
    step_val = 0

    _conditions = (
        step_cond,
    )

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        '''
        step_val was changed by the machine.
        '''

        self.step_val += 1
        print '{} heard {} {}'.format(self, condition, self.step_val)


import time


class EconomyMachine(Machine):

    step_frame = 10
    _step = 0

    def start(self):
        self._step = 0
        while 1:
            time.sleep(1)
            self.step()

    def step(self):
        '''
        Step a time of the machine
        '''
        self._step +=  self.step_frame
        # print 'step', self._step
        # We can bridge the gap to event dispatch by calling all calendar
        # nodes and stepping. All
        calendar_nodes = self.nodes.get('calendar')
        for cn in calendar_nodes:
            cn.step_val = self._step


def run():

    ma = EconomyMachine('example')
    generate_people(ma)
    ma.start()
    return ma


def generate_people(machine, count=100):
    print 'generating {} people'.format(count)
    for index in range(count):
        name = "p{}".format(index)
        person = Person(name='person')
        person.index = name
        person.step_val = machine._step
        machine.nodes.add(person)
    machine.nodes.add(CalendarNode(name='calendar'))
    print 'generated {} people'.format(count)


def main():
    global g
    g = run()
    print g


if __name__ == '__main__':
    main()
