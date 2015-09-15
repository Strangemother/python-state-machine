from runner import Runner

import sys
global g

if __name__ == '__main__':
    ar = sys.argv
    r = Runner()
    if len(ar) > 1:
        g = r.run(ar[1])
    else:
        print 'running root'
        from root import *
        from examples.basic import run
        m = run()
        n = m.nodes.get('TestNode')[0]



