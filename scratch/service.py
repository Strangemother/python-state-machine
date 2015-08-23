import rpyc

class FooService(rpyc.Service):

    ALIASES = ["floop", "bloop"]

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        print 'on_connect'

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        print 'on_disconnect'

    def exposed_get_answer(self): # this is an exposed method
        print 'Get answer'
        return 42

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(FooService, hostname='0.0.0.0', port = 18861)
    print 'Start Service'
    t.start()
