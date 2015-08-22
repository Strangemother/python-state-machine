import sys
from runner import Runner

global g

if __name__ == '__main__':
    ar = sys.argv
    r = Runner()
    if len(ar) > 1:
        print ar
        g = r.run(ar[1])
    else:
        print 'running root'
        from root import *
        from examples.e1 import run
        m = run()
        n = m.nodes.get('TestNode')[0]


