import sys
from runner import Runner

if __name__ == '__main__':
    ar = sys.argv
    r = Runner()
    r.run(ar[1])
    