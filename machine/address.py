'''
An address helps couple a message to a location. By parsing and
creating strings to be manipulated by the bridge
'''
import copy
from collections import deque, namedtuple

AddressParts = namedtuple('AddressParts', 'prefix nodes machines')

def make_hash(o):

    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).
    """

    if isinstance(o, (set, tuple, list)):
        return tuple([make_hash(e) for e in o])

    elif not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))

class Address(object):

    SEP = '.'
    JOIN_SEP = '+'

    def set_join_seperator(self, v):
        self._invalid_cache = True
        self._join_seperator = v

    def get_join_seperator(self):
        return self._join_seperator


    def set_seperator(self, v):
        self._invalid_cache = True
        self._seperator = v

    def get_seperator(self):
        return self._seperator

    join_seperator = property(get_join_seperator, set_join_seperator)
    seperator = property(get_seperator, set_seperator)


    def __init__(self, name=None, *args, **kw):

        self.name = name
        self._path = kw.get('path', None)
        self._cache_hash = None
        self._invalid_cache = True
        self._parts = None #AddressParts

        self.machine = kw.get('machine', None)
        self.machines = kw.get('machines', [])
        self.node = kw.get('node', None)
        self.nodes = kw.get('nodes', [])

    def _parse(self, name=None, **kw):
        '''
        Parse the value into an addressable
        '''
        # String name provided to the Address
        name = kw.get('name', name or self.name)
        name = '' if name is None else name

        # Spliting the prefix, nodes and machine
        sep = self._get_seperator()
        #
        sp = deque(name.split(sep))

        _prefix = sp.popleft() if len(sp) > 0 else None
        nodes = kw.get('nodes', None) or []
        machines = kw.get('machines', None) or []
        _node = None

        if _prefix == 'node':
            if len(sp) > 0:
                _node = sp.pop()
            else:
                _node = _prefix

        elif _prefix != 'machine':
            # prefix of machine or no prefix
            sp.appendleft(_prefix)
            # print 'not machine, sp appendleft:', _prefix
            # nodes.append(_prefix)
            _prefix = 'node'
            _node = sp.pop()
            # print 'Node is', _node

        for m in list(sp):
            ml = m.split(self.JOIN_SEP)
            for machine in ml:
                # print 'add machine', machine
                machines.append(machine)

        _n = '' if _node is None else _node
        nl = _n.split(self.JOIN_SEP)
        # print 'names', nl
        for node in nl:
            if len(node) > 0: nodes.append(node)

        ap = AddressParts(_prefix, nodes, machines)
        # print 'ap', ap
        return ap

    def _make(self, machines=None, nodes=None, machine=None, node=None, name=None):
        '''
        create an address string passing arguments to manage with.

        Using make without implementing self references can genenerate
        an Address without altering the original Address - similar to
        a factory
        '''

        ms = machines or []
        ns = nodes or []

        # Seperator of string defined names
        join_sep = self.join_seperator if hasattr(self, 'join_seperator') else Address.JOIN_SEP
        path_sep = self.seperator if hasattr(self, 'seperator') else Address.SEP

        fa = self._parse(name or self.name, **{
                'machines': machines,
                'machine': machine,
                'nodes': nodes,
                'node': node
            })

        # Cleaner stringly output placholder
        output = AddressParts(fa.prefix, [], [])

        # get the machine and append it
        m = machine.name if hasattr(machine, 'name') else machine
        if m is not None: output.machines.append(m)
        print 'added machine to output', m

        # Iterate provided machines list
        for m in fa.machines:
            nm = m
            if hasattr(m, 'name'): nm = getattr(m, 'name')
            # add the name to the output
            print 'add another machine', nm
            output.machines.append(nm)

        # Iterate provided nodes.
        for n in fa.nodes:
            nm = n
            # Get the name of the node though the function
            if hasattr(n, 'get_name'): nm = getattr(n, 'get_name')()
            # append it to the output
            print 'add node from passed nodes', n
            output.nodes.append(nm)

        # Get the node and append it
        n = node.get_name() if hasattr(node, 'get_name') else node
        # append the name to the output
        if n is not None: output.nodes.append(n)
        print 'added a node', n

        prefix = 'machine'
        # auto define  if there are nodes.
        if len(output.nodes) > 0:
            prefix = 'node'


        # Create string parts for path
        nj = join_sep.join(output.nodes)
        mj = join_sep.join(output.machines)
        # String path - will always have a prefix of machine or node.
        pa = [prefix]
        # Add the strings to the combination path; omiting blanks.
        if mj is not None and len(mj) > 0: pa.append(mj)
        if nj is not None and len(nj) > 0: pa.append(nj)

        # create the path
        if path_sep is None: path_sep = ''
        path = path_sep.join(pa)

        self._parts = output
        # Return a path with these arguments applied
        self._path = path
        self._invalid_cache = False

        return self

    def _args_obj(self, **kw):
        '''
        return a dict of arguments used to generate the address data.
        This is used by str, path and repr functions
        '''
        nodes = self.nodes
        machines = self.machines
        if self._parts:
            nodes = self._parts.nodes
            machines = self._parts.machines

        obj = {
            'machine': kw.get('machine', self.machine),
            'machines': kw.get('machines', machines),
            'node': kw.get('node', self.node),
            'nodes': kw.get('nodes', nodes),
            'name': kw.get('name', self.name)
        }

        return obj

    def _get_seperator(self):
        s = self.seperator if hasattr(self, 'seperator') else self.SEP
        return s

    def _get_join_seperator(self):
        s = self.join_seperator if hasattr(self, 'join_seperator') else self.JOIN_SEP
        return s

    def __hash__(self):
        d = self._args_obj()
        d['sep'] = self._get_seperator()
        d['join_sep'] = self._get_join_seperator()
        h = make_hash(d)
        return h

    def build(self, **kw):
        '''
        Build the address str based up on provides arguments.
        '''
        args = self._args_obj(**kw)
        return self._make(**args)

    def path(self, **kw):
        if self._invalid_cache: self._cache(**kw)
        return self._path

    def _cache(self, **kw):
        '''
        Rebuild the internal elements to ensure strings and references
        match internal lists.
        '''
        self.build(**kw)

    def __str__(self):
        return str(self.path())

    def __repr__(self):
        kw = {
            'path': self.__str__()
        }

        f = "<machine.Address '{path}'>"
        s = f.format(**kw)
        return s
