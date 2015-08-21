g = None
rc =  None

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
        g = run()
        return g

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

    def rpc(self):
        from examples.rpc import main
        print 'running rpc'
        global g
        global rc
        import rpyc as r
        rc= r
        g = main()
        return g


    def machine(self):
        from examples.basic import run
        return run()

    def clock(self):
        from examples.clock import run
        return run()

    def conds(self):
        from machine.managers import ConditionsManager
        from conditions import Condition
        from pprint import pprint

        cds = ConditionsManager()
        c= Condition('foo', 'bar',3)
        cds.append_with_names( ('wibble', 'tos',), c)
        pprint(cds._names)
        return cds
