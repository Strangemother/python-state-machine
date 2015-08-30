
class ProxyBase(object):
    pass


class ProxyNode(ProxyBase):
    '''
    A Proxy machine maintains an active connection
    through a bridge calling methods through the
    local machine to the target machine.
    You could send events through your local machine -
    but it's easier to use a Proxy type.
    '''
    _connection = None

    def __init__(self, name=None):
        self.name = name
