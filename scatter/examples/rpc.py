import rpyc


def main():
    print 'Run rpc service'
    c = rpyc.connect('0.0.0.0', 18861)
    print dir(c)
    return c

if __name__ == '__main__':
    main()
