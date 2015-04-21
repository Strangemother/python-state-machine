from base import Base
from constants import *
from tools import random_string
import inspect
from itertools import izip as zip, count



class Nodes(list):
    '''
    A Nodes class handles many Node objects for the machine or any
    provider for the requirement of the node tree
    '''
    def __init__(self, name=None, nodes=None):
        self.name = name or random_string(4)

        if nodes is not None:
            self.extend(nodes)

    def get(self, name):
        '''
        return a node by key.
        '''
        names = [x.get_name() for x in self]
        nodes = Nodes(nodes=[i for i, j in zip(self, names) if j == name])
        return nodes
        # return self[names.index(name)]

    def set(self, key, value):
        '''
        Change the key value of all the internal set.
        '''

        for node in self:
            node.set(key, value)


class ConditionManager(object):
    '''
    An iterable of conditions defines key value changes to react to.
    '''
    _conditions = None

    def get_conditions(self):
        '''
        return an iterable of conditions to be applied against this node
        '''
        if hasattr(self, '_conditions') and getattr(self, '_conditions') is not None:
            return self._conditions
        return []

    def cache_conditions(self, conds):
        '''
        create a list of condition names based upon the provided
        conditions. if the order of the conditions change this method
        should be called to revalidate the names list reference.

        returned is a list of named from the iterated Conditions.
        self._cache_conditions is populated with the names list.
        '''
        self._cache_conditions = [x.get_name() for x in conds]
        return self._cache_conditions

    def get_condition_by_name(self, name):
        '''
        return the conditions matching the name provided.
        The name is a reference to the node, key, state - returned from
        Condition.get_name().

        Zero or more items will be returned in a list.
        '''
        cnds = self._cache_conditions
        if name in cnds:
            cnd = self.get_condition_by_position( cnds.index(name) )
            return cnd
        return None

    def get_condition_by_position(self, position):
        '''
        Return a condition based upon its index within the list of
        assigned positions.
        '''
        cnds = self.get_conditions()
        return cnds[position]


class Node(Base, ConditionManager):
    '''
    A node exists on the network, serving data attributes to
    read in the network.
    '''
    name = None
    state = Status.NEW

    def __init__(self, name=None, events=None):
        self.log_color = 'blue'
        from events import e
        self._valid=False
        self.events = events or e
        self.name = name or self.get_name()

    def met_condition(self, machine, condition):
        # each node provided by get() from machine.
        cnd = self.get_condition_by_name(condition)
        print 'Met', cnd, 'for', self
        # valid = node.react(self.machine, condition=cnd)

    def get_validation(self, machine, condition):
        r = {}
        valid = len(self.get_conditions())>0

        for cnd in self.get_conditions():
            v, reason = cnd.validate(machine=machine, node=self, condition=condition)
            r[cnd.get_name()] = [v, reason]
            if v is False: valid = False
        return (valid, r, )

    def react(self, machine, condition=None):
        '''
        React can be called to make this not fire it's
        validation and. This will fire events into the network for other
        nodes to listen.

        condition is optional for the method but may be required by the
        network node target.
        This condition defines the reactive to cause a Node.react
        '''
        self.log(self, 'reacting to', machine, condition)

        valid, reason = self.get_validation(machine, condition)
        if valid is not True:
            return False
        # check machine conditions for the keys.

        names = ['%s.%s:%s' % (self.get_name(),x, self[x]) for x in self.get_attrs()]

        reg = machine.register.conditions

        for cn in names:
            node_names = reg.get(cn)
            if node_names is None:
                continue

            for name in node_names:
                self.log(cn, 'for', name)
                ns = machine.nodes.get(name)
                for node in ns:
                    # import pdb; pdb.set_trace()
                    print 'Render reaction', condition, cn
                    node.react(machine, cn)
        self.set_validated(valid)

        return valid

    def set_validated(self, valid):

        if valid:
            if self._valid is not valid:
                self.valid()
                self.dispatch('valid', self)
            else:
                self.invalid()

        self._valid = valid

    def valid(self):
        '''
        Method to override a success valid.
        '''
        return self._valid

    def invalid(self):
        '''
        Method to override for an unsuccessful validation
        '''
        return self._valid != True

    def get_name(self):
        if self.name is None:
            return self.__class__.__name__# random_string(4)
        return self.name

    def set(self, key, value, condition=None):
        '''
        change a node value
        '''
        self.log('SET', self.get_name(), key, '=', value)

        sn = '%s.%s:set' % (self.get_name(), key)
        self.dispatch(sn)

        setattr(self, key, value)
        kn = '%s.%s:%s' % (self.get_name(), key, value)
        self.dispatch(kn)

        cn = '%s.%s:changed' % (self.get_name(), key,)
        self.dispatch(cn, key=key, value=value, condition=condition)
        # self.events.dispatch(cn, key=key, value=value)

        return getattr(self, key, value) == value

    def dispatch(self, name, *args, **kwargs):
        kwargs['node'] = self.get_name()
        self.events.dispatch(name, name, *args, **kwargs)

    def integrate(self, machine=None):
        '''
        Integrate this node to the current machine. Mapping the
        structure and starting the reactions.
        '''
        # machine.events.dispatch('expose', expose=self.exposed() )
        self.dispatch('expose', expose=self.exposed() )
        conds = self.get_conditions()
        if conds:
            self.cache_conditions(conds)
        return self

    def __str__(self):
        return 'Node %s "%s"' % (self.__class__.__name__, self.name, )

    def __getitem__(self, k):
        return getattr(self, k)

    def exposed(self):
        '''
        return an array of attributes from this class defining exposed
        fields for node networking
        '''
        return self.get_attrs()

    def get_attrs(self):
        '''
        Find all key attrs
        '''
        ignore = Node.__dict__.keys()
        # ignore = reduce(lambda x, y: x+y, [x.__dict__.keys() for x in iter(classes)])
        fields = []
        classes = self.__class__.__mro__
        # rint classes
        for parent_class in iter(classes):
            # print 'class', parent_class
            keys = parent_class.__dict__.keys()
            ckeys = self.__class__.__dict__.keys()
            for model_field in keys:
                is_cls = inspect.isclass(getattr(parent_class, model_field))
                is_meta = model_field == 'Meta' and is_cls
                name = model_field
                if is_meta or model_field in ignore or model_field.startswith('__'):
                    continue
                if model_field in ckeys:
                    fields.append(name)

        for field in ignore:
            name = field
            if field in ignore or field.startswith('__'):
                continue
            ignore.append(name)
        return fields


class Walker(Base):
    '''
    A walk helps traverse a Node and its condition tree to find issues
    and circular references.
    '''
    base_node = None

    def __init__(self, node=None):
        '''pass a base_node to begin the path'''
        self.base_node = node

    def walk(self, machine=None, node=None, recurse=True, recurse_count=0):
        node = node or self.base_node

        if node is None:
            raise Exception('Walker needs a node')
            return None
        cds = node.get_conditions()
        cdd = {}

        for cd in cds:
            # Map the node conditions tree.
            d= {}
            d['node'] = cd.node
            if recurse and recurse_count < 2:
                cc = recurse_count + 1
                d['conditions'] = [Walker(x).walk(machine, recurse_count=cc) for x in machine.nodes.get(cd.node)]
            d['state'] = cd.state
            d['condition'] = cd.get_name()

            if machine:
                d['init_state'] = [x[cd.key] for x in machine.nodes.get(cd.node)]
                d['init_ready'] = True
            else:
                d['init_ready'] = False

            cdd[cd.get_name()] = d
        self.log('Node Data', node)
        return cdd
