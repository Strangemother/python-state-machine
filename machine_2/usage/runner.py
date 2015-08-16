from machine import Machine


class Runner(object):

    def run(self, cmd, *args, **kwargs):

        m = getattr(self, cmd)
        if m is not None:
            return m(*args, **kwargs)

    def ran(self):
        self._ran = True
        return True


    def hello(self):
        s = 'Hello?.. Are you there?.. Can you hear me?..'
        return s

    def machine(self):
        print 'running machine'
        print Machine('example')
