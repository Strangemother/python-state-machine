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
        g = r.run('hello')
