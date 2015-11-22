from subprocess import call
import os


def gen_tests():
    '''
    Generate the sphinx docs
    '''
    dirn = os.path.dirname(os.path.realpath(__file__))
    p = os.path.join(dirn, '..')
    cwd = os.path.abspath(p)
    print 'Generating on:', cwd

    s = 'pythoscope scatter'
    call(s.split(' '), cwd=cwd)
    print 'running tests'
    ts = 'nosetests scatter --with-coverage --cover-erase'
    call(ts.split(' '), cwd=cwd)

if __name__ == '__main__':
    gen_tests()
