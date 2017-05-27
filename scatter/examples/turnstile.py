from scatter import Node, Condition

LOCKED = 'LOCKED'
UNLOCKED = 'UNLOCKED'


class Turnstile(Node):
    state = LOCKED
    cost = 50
    input_coins = 0
    turns = 0

    _conditions = (
            Condition('state', Condition.CHANGED, 'state_changed'),
            Condition('turns', Condition.POSITIVE, 'turns_positive'),
            Condition('input_coins', Condition.CHANGED, 'input_coins_changed'),
        )

    def state_changed(self, node, key, nv, ov, *args, **kw):
        if nv == LOCKED:
            print 'Locked. Insert coin.'
        elif nv == UNLOCKED:
            print 'Allow push'

    def input_coins_changed(self, node, key, nv, ov, *args, **kw):
        print 'Total:', nv
        if nv >= 50:
            self.state = UNLOCKED
        else:
            self.state = LOCKED

    def turns_positive(self, *args, **kw):
        print 'Turned, swallow money'
        self.input_coins -= self.cost

    def push(self):
        if self.state == UNLOCKED:
            print 'person pushed open'
            self.turns += 1
        else:
            tc = self.cost - self.input_coins
            print 'Need', tc, 'to open'

    def coin(self, val):
        print 'inserted', val
        self.input_coins += val


def run():
    n = Turnstile()
    print '... Next Person'
    n.push()
    print '... Money'
    n.coin(20)
    n.coin(20)
    print '... Test'
    n.push()
    n.coin(20)
    n.push()
    print '... Next Person'
    n.push()
    return n


def main():
    global g
    g = run()
    print g


if __name__ == '__main__':
    main()
