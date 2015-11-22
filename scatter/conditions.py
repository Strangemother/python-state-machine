'''
A condition
'''
from compares.const import register_compare, Const as const
from compares.simple import Exact
from collections import OrderedDict
from inspect import isclass, ismethod


calldict = {}

class Stack(const):

    def stack_add(self, cb, cbargs):
        '''
        Pass the values of which would be provided to the callback.
        The callback and its arguments are added to a singleton stack
        of callbacks of which should fire.

        After the natural fire-events, one or many callbacks may have been
        skipped. These members methods and functions are chacked against the
        stack. If they exist the standard runner did not call the method.

        This may occur if the callback has an error of which was lost through
        the event chain. In good operation this stack will always be empty.
        '''
        # check callback assignments. Providing flag values from
        # attr
        # We should provide this as arguments as it's flagged as special.

        # There seems to be a special little bug where:
        #  if more than one event is occuring at the same time, the event
        #  callback will not fire.
        #  The first print line will occur and then nothing.
        #
        #  I've been debugging this for a while so intead, a dictionary stack
        _id = id(self)
        if calldict.get(_id) is None:
            calldict[_id] = {
                id(cb): [ cb, cbargs ],
            }

        return _id

    def stack_call(self):
        '''
        Call every stack method within the calldict singleton.
        '''
        for missed_call in calldict:
            func_set = calldict[missed_call]
            # cb(args)
            for func_id in func_set:
                caller = func_set[func_id]
                print 'calling from stack', caller[0]
                caller[0](*caller[1])
            else:
                print 'No skipped results'

    def stack_remove(self, _id):
        '''
        Remove the stack entity by reference of the provided _id from the
        calldict singleton.
        This _id was previously provided by self.stack_add
        '''
        # Delete ourselves as the successor.
        del calldict[_id]
        # Rerun undone


class Condition(Stack):
    ''' A condition perpetuates changes of an object base upon
    rules applied at configuration.

        Condition('foo', Condition.CHANGED, 'foo_changed')
        Condition('bar', 2, foo_callback, node='ANode')
    '''

    state = None

    def __init__(self, attr=None, value=None, valid=None, node=None, name=None, **kw):
        ''' A condition requires
        a node (Node|String|iterable),
        the attribute to monitor (String),
        a value to validate condition.

        Optionally `valid` callback when the condition is met

        You can add keyword args to provide additional validations to the condition.
        '''
        self._keys = OrderedDict()
        self.valid_cache = {}
        # the node to watch for changes.
        self.node = node
        # Attrbibute to monitor on node.
        self._attr = attr
        # Assign the constant type to match - or the target value to validate to.
        self._value = value
        # A def callback - if any
        self._valid_cb = valid
        self._last = False
        if valid is not None:
            print 'Valid on condition', valid
        self.name = name
        self.read_args(**kw)

    def read_args(self, **kw):
        '''provide keyword arguments for the condition to match.
        The value of a keyword may be a primitive python object or a Compare.
        '''
        attr = self._attr
        value = self._value
        if attr is not None:
            self.store_statement(attr, value)
        for key in kw:
            self.store_statement(key, kw[key])

    def store_statement(self, key, value):
        ''' Store a statement into the condition to be met when the condition
        is run '''
        self._keys.update({key: value})
        return self._keys

    def match(self, current, incoming, node, key, expand=False, parent_node=None):
        ''' This method is to be used outside the reference scope. Called by
        a node alteration or a machine call, the match() method will
        return a validation based upon provided values and the internal
        self.value statements.

        current is the value existing within the node[key].
            This value could be collected again, but to protect against any
            future complex implementation of a Node, we have an early
            definition to check.
        incoming is the value node[key] will become after match()
            A condition is called prior to the value being written to a Node.
            We're defining ahead of time if this statement will be true.
        node is the context object to match the condition
        key is the attr within the node object this condition is matching.
            The Node blindly runs this method. We check if the key is
            something we wish to use before performing validity.
        expand returns the valids object if True else a boolean if False
            passing true, you can see which statements failed within the
            condition.
        parent_node is the node this condition exists within.
            If a condition exists within a node, when the parent node is ran
            for changes, it passes a reference to the matcher.
            This allows string references within the condition to be dynamic

        returned is a boolean value of validity. '''
        if key not in self._keys.keys():
            return self._last

        valids = self.run_statements(node, key, current, incoming)


        # flatten the dict in to a set of True/False
        vlist = list(set(valids.values()))

        # Both True/False exist
        if len(vlist) > 1:
            return False

        if vlist[0] is True:
            self._call_handler(node, valids, key, incoming, current, parent_node)

        if expand:
            return valids
        # Return the one statement
        self._last = vlist[0]
        return self._last

    def _call_handler(self, node, valids, key, incoming, current, parent_node=None):
        ''' Call the handler with the node, value and field passed.
        If the self._valid_cb is a string the method is received from the node
        and called. '''
        cbn = self._valid_cb
        cb = cbn
        parent = parent_node or node
        if isinstance(cbn, (str, unicode,)):
            cb = getattr(parent, cbn)

        if cb is None:
            print 'Could not find callback method', cbn
            return

        _id = self.stack_add(cb, [node, key, incoming, current, valids])
        # Will fire
        cbv = cb(node, key, incoming, current, self, valids)
        # Successful will fire
        self.stack_remove(_id)
        # self.stack_call()

    def run_statements(self, node, key, current, incoming):
        ''' Iterate the statements collecting boolean values.
        Returned is a a bool of validity.
        Pass expand=True to return an object of key values. Each key is
        an attr of the node with its boolean return.

        node is the object of context.
            This is syntax sugar and probably not required.
        key is the attr within the node
        current is the existing value within the node[key]
        incoming is the future value the node[key] will become after validity'''

        valids = {}

        for _key in self._keys:
            if _key == key:
                value = self._keys[_key]
                res = self.check_statement(node, _key, value, current, incoming)
                self.valid_cache[_key] = res
                valids[_key] = res
            else:
                # populate the validity object with previously checked conditions.
                # # If None the attr has never been set on the condition therefore
                # the statement is False.
                valids[_key] = self.valid_cache.get(_key, False)
        return valids

    def check_statement(self, node, key, value, current, incoming):
        ''' check_statement returns boolean of the key, value passed.

        The node is the element to check the condition statement against.
        The key is the attr within the node of which will change to the value.
        The value is the stored comparison value to check against.

        current is the existing value within the node[key]
        incoming is the future value the node[key] will become after validity

        The node[key] contains the existing value of the key attr. This may
        change after this statement has returned its validity.

        it's most likely to check the incoming value rather than the current.
        The condition is pre checked ensuring any later nodes within a chain
        denotes this conditions validity. '''

        # print 'Checking condition against node', self.node, ' input:', node
        if self.node is not None:
            # Is this our context node to matcn
            is_node = node.get_name() == self.node or self.node == node
            if is_node is False:
                # print '\nX  Node does not match', self.node, node
                return False
            # else:
            #     print'\nY  Good match Continue validation'

        Klass = Exact
        matching_val = value

        if isinstance(value, tuple):

            _K = self.get_comparison_class(value[1])
            # print 'Using', _K
            if isclass(_K) and ismethod(_K.match):
                Klass = _K
                matching_val = current
            else:
                print 'Not a matching class', _K, value

        comp = Klass(self)
        s = '++ statement {0} val:{1} - Using: {2}({3}, {4})'
        ps = s.format(key,
                       value,
                       comp.__class__.__name__,
                       incoming,
                       matching_val
                       )
        # print ps
        valid = comp.match(incoming, matching_val)
        # print 'valid', valid
        return valid

    def get_comparison_class(self, compare):
        '''
        Return the compare class by string
        '''
        m = __import__('scatter.compares.simple', fromlist=[compare])
        k = getattr(m, compare)
        return k

    def valid(self, value=None):
        return self.match(value, self.value, self.node, self.attr)

    def __str__(self):
        t = self._value

        if isinstance(t, (list, tuple)):
            t = self._value[1]

        s = '{1}:{2}'.format(self.node, self._attr, t)
        return s

    def __unicode__(self):
        return u'%s' % self.__str__()

    def __repr__(self):
        s = self.name if self.name is not None else self.__str__()
        return '<Condition: %s>' % (s,)
