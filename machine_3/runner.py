g = None
rc =  None

class Runner(object):

    def run(self, cmd, *args, **kwargs):

        try:
            m = getattr(self, cmd)
        except AttributeError as e:
            m = None

        if m is not None:
            return m(*args, **kwargs)
        else:
            import examples as _e
            m = __import__('examples', fromlist=[cmd])
            _k = [x if x.startswith('__') is False else None for x in dir(_e)]
            keys = filter(None, _k)
            if cmd in keys:
                # get the module
                runmod = getattr(_e, cmd)

                if hasattr(runmod, 'main'):
                    return runmod.main()
                if hasattr(runmod, 'run'):
                    return runmod.run()
                else:
                    print 'Could not run module', cmd

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

    def conds(self):
        from machine.managers import ConditionsManager
        from conditions import Condition
        from pprint import pprint

        cds = ConditionsManager()
        c= Condition('foo', 'bar',3)
        cds.append_with_names( ('wibble', 'tos',), c)
        pprint(cds._names)
        return cds
