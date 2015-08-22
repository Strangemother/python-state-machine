from base import Base
from blinker import ANY, signal

class Events(Base):
    ALL = ANY

    def __init__(self):
        self.signals = {}
        self.log_color = 'cyan'

    def dispatch(self, name, *args, **kwargs):
        '''
        Dispatch an event to be propogated through the network.
        A set of args and
        '''
        # self.log('Dispatch', name)
        s = self.signals.get(name)
        if s:
            s.send(*args, **kwargs)
        else:
            pass
            # import pdb; pdb.set_trace()
            # check existing conditions
            self.log('Signal', name)



    def listen(self, name, receiver, sender=None):
        '''
        Listen to a 'name' event to occur. The receiver will be exectuted.
        The receiver will be called ever time the 'name' event is heard.
        To listen to a specific 'sender'. Pass the name of the sender
        '''
        self.log('listen to', name)

        _signal = self.signals.get(name)
        if _signal is None:
            self.signals[name] = signal(name)

        if sender is None:
            self.signals[name].connect(receiver)
        else:
            self.signals[name].connect(receiver, sender=sender)
