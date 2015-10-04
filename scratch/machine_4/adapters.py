import Pyro4


class PyroAdapter(object):

    _nameserver = False

    def __init__(self):
        self._daemon = None

    def setup_pyro(self):
        import config as _c
        _k = [x if x.startswith('__') is False else None for x in dir(_c)]
        keys = filter(None, _k)
        for name in keys:
            setattr(Pyro4.config, name, getattr(_c, name))

    def daemon(self):
        if self._daemon is None:
            self.setup_pyro()
            self._daemon = Pyro4.Daemon()
        return self._daemon

    def register(self, item):
        if self._daemon is None:
            self.daemon()
        return self._daemon.register(item)

    def get_nameserver(self):
        if self._daemon is None:
            self.setup_pyro()
        try:
            return Pyro4.locateNS()
        except Pyro4.errors.NamingError:
            # no name server
            return None

    def get_object(self, uri):
        o = Pyro4.Proxy(uri)
        return o
