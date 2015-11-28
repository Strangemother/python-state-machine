from scatter import Machine, Node, Condition


class OnNode(Node):
    on = False

    def conditions(self):
        c = (
            Condition('on', Condition.CHANGED, 'on_changed'),
        )

        return c

    def on_changed(self, node, key, new_val, old_val, condition, valids):
        '''
        color changed condition handler. Will fire when any node.color alters.
        '''
        print 'house', new_val


def run():
    ma = House()
    return ma


def main():
    global g
    g = run()


if __name__ == '__main__':
    main()
