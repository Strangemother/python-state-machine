from scatter import Machine, Node, Condition

step_cond = Condition('step_val', Condition.CHANGED, 'step_changed')

class PersonNode(Node):

    _conditions = (
        Condition('color', Condition.CHANGED, 'color_changed', node='person'),
    )

    def color_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        print '{} heard {} {}'.format(self.index, condition, new_val)

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        '''
        A calendar has stepped time to a value specified.
        '''
        print '{} heard {} {}'.format(self.index, condition, new_val)



class Person(PersonNode):

    _conditions = (
        Condition('minutes', Condition.CHANGED, 'calendar_weeks_changed', node='calendar'),
        step_cond,
    )

    age = 20
    step_val = 0

    def calendar_weeks_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        if self.index == 40:
            print 'minute', new_val

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        self.step_life(node, new_val)

    def step_life(self,node, val):
        self.step_val = val
        if self.index == 40:
            age = node.years + self.age
            if age != self.age:
                print  self.index, 'person(40) Birthday', self.age


class CalendarNode(Node):

    # seconds
    step_val = 10

    years = 0
    months = 0
    minutes = 0
    seconds = 0

    _conditions = (
        step_cond,
    )

    def step_changed(self, node, key, new_val, old_val, condition, valids, **kw):
        '''
        step_val was changed by the machine.
        '''

        secs = self.step_val + 1
        mins = secs / 60
        hours = mins / 60
        days = hours / 60
        weeks = days / 7
        months = weeks / 7
        years = months / 12

        print 'secs {}, mins {}, hours {}, days {}, weeks {}, months {}'.format(secs, mins, hours, days, weeks, months)

        self.seconds = secs
        self.minutes = mins
        self.hours = hours
        self.days = days
        self.weeks = weeks
        self.months = months
        self.years = years



import time


class EconomyMachine(Machine):

    step_frame = 10
    _step = 0

    def start(self):
        self._step = 0
        while 1:
            # time.sleep(1)
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
        person = Person(name='person')
        person.index = index
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
