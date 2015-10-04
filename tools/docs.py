from subprocess import call
import os


def gen_docs():
    '''
    Generate the sphinx docs
    '''
    dirn = os.path.dirname(os.path.realpath(__file__))
    p = os.path.join(dirn, '..')
    cwd = os.path.abspath(p)
    print cwd
    s = 'sphinx-apidoc -o autodocs/build scatter'
    call(s.split(' '), cwd=cwd)

    s = 'sphinx-build autodocs/source autodocs/build'
    call(s.split(' '), cwd=cwd)

if __name__ == '__main__':
    gen_docs()
