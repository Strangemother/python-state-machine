
class Runner(object):

    def run(self, cmd, *args, **kwargs):

        m = getattr(self, cmd)
        if m is not None:
            return m(*args, **kwargs)

    def ran(self):
        self._ran = True
        return True

    def help(self):
        print 'Run the state machine: python machine [command]'
        keys = dir(self.__class__)
        pkeys = [x if x.startswith('__') is False else None for x in keys]
        ks =  filter(None, pkeys)
        for x in ks:
            print '{0}'.format(x)

    def hello(self):

        s = 'Hello?.. Are you there?.. Can you hear me?..'
        return s

    def car(self):
        from examples.car import run
        print 'running car'
        run()

    def chain(self):
        from examples.chain import run
        print 'running chain'
        run()


    def direction(self):
        from examples.direction import run
        print 'running direction'
        run()

    def simple(self):
        from examples.simple import run
        print 'running simple'
        return run()

    def machine(self):
        from examples.basic import run
        return run()

        return ma
