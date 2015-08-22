class Status:

    '''
    NEW defines a node og which has been created without adding
    to the network. An initial Node will have the status of NEW
    '''
    NEW = 'new'

class State:
    '''
    Internal node state changes to monitor.
    '''

    # when a node changes
    CHANGED = 'changed'
