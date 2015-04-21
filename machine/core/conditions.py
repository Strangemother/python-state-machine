from base import Base
from constants import State

'''
A condition is a key of a node to monitor for a state.
When all conditions are met within a node,
the reaction will occur.
'''

class Condition(Base):

    def __init__(self, node, key, state=State.CHANGED, callback=None):

        # The node to monitor. This could be
        # class or string.
        self.node = node

        # Key of node to monitor for change.
        self.key = key

        # state of the condition to validate a true
        # Condition and react
        self.state = state

        # can be method or string. If a method is passed, it's converted
        # to a string to be later referenced.
        self.callback = callback

    def get_name(self):
        return '%s.%s:%s' % (self.node, self.key, self.state)

    def __str__(self):
        return 'Condition %s' % (self.get_name())

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__module__, self.__str__())

    def validate(self, machine, node, condition=None):
        '''
        return boolean to determin if this condition has been met.

        A node is required to validate against. This would be the
        parent to validate against. Naturally a condition will exist within
        a node, therefore passing the parent node is essentially checking
        a nodes conditions. But any node will do.

        The name of the condition self.node will be validated.

        machine     a react() method calls passing the node machine
        node        The parent node passed
        condition   The condition making this condition validate
        '''
        # monitor node
        mns = machine.nodes.get(self.node)

        if len(mns) == 0:
            return (False, 'no machine node %s' % self.node)

        for node in mns:
            # the node must exist for the condition to validate
            if node is None:
                return (False, '%s node in %s' % (self.node, machine) )

            # the key must exist on the node
            if hasattr(node, self.key) is False:
                return (False, '%s.%s is missing' % (node.name,self.key) )

            # self.state must be the value of the node key
            if getattr(node, self.key) != self.state:
                return (False, '%s.%s is not state %s' % (node.name,self.key, self.state) )


            # self.log('Valid Condition', self.get_name())
            if self.callback is not None:

                # import pdb; pdb.set_trace()
                '''
                Call the callback provded to the Condition when True.
                The method is called providing

                node        node provided for validation
                self        condition validating
                condition   Condition causing validation

                '''
                self.callback(node, self, condition)

        return (True, 'valid')
