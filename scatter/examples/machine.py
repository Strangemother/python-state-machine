'''
This example shows how to implement a node to a machine.
The TestNode contains a value "color".

The condition will react when 'color' is changed on the node.

    g.nodes[0].color = 'green'
    # 'Color changed from blue to green'
'''
from scatter.remote import PyroAdapter
from scatter import Machine, Node, Condition
import os.path
import os
import pickle


class ReactNode(Node):
    _conditions = (
            Condition('koo', Condition.CHANGED, 'foo_changed'),
        )

    def foo_changed(self, node, key, current, incoming, *args):
        print 'ReactNode', key

names = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


def mem_pickle(o=None):
    '''
    Receive an object. to store to.
    passing back an object will picke save
    '''
    fp = 'last_remote.p'
    if o is None:
        if os.path.isfile(fp):
            return pickle.load(open(fp, 'rb'))
        return {}
    else:
        pickle.dump(o, open(fp, 'wb'))


def get_next_name(list):
    '''
    Get the next name in the list of which has not been allocted in the
    mem_pickle
    '''
    pl = mem_pickle()
    for abbr, name in list:
        e = abbr in pl
        if e is False:
            break
    return abbr


def get_file_line(p):
    uri = None
    with open(p, 'r') as f:
        uri = f.readlines()
    return uri[0]


def run():
    nm = get_next_name(names)
    print 'Creating machine', nm
    m = Machine(nm)
    n = Node('woo')
    n2 = ReactNode('Dibble')
    m.nodes.add(n)
    m.nodes.add(n2)
    print 'wait() functon setup'
    print 'connect() functon setup'

    return m

def wait():
    _uri = g.adapter.get_uri()
    pp = 'last_remote.txt'
    f = open(pp, 'w')
    f.write(str(_uri))
    f.close()
    po = mem_pickle()
    po[g.name] = _uri
    po['last'] = (g.name, _uri)
    print 'waiting as', g.name, _uri
    mem_pickle(po)
    g.wait()

def connect():
    '''
    Connect the machine to the last 'wait()' machine.
    The list file is inspected for last started.
    '''
    po = mem_pickle()
    print 'connecting to', po['last'][0]
    g.adapter.add(po['last'][0], po['last'][1])
    global n
    n = g.nodes[0]
    n.foo = 2

def adapter():

    # a = PyroAdapter('foo')
    m = run()
    global uri
    _uri = m.adapter
    uri = _uri
    print 'URI', _uri
    pp = 'last_remote.txt'

    if os.path.isfile(pp):
        # use value
        ur = get_file_line(pp)
        g = a
    else:
        f = open(pp, 'w')
        f.write(str(_uri))
        f.close()
        print 'waiting', _uri

        try:
            m.wait()
        except KeyboardInterrupt:
            pass

        uri = get_file_line(pp)
        if uri == _uri:
            os.remove(pp)


if __name__ == '__main__':
    global g
    g=run()
