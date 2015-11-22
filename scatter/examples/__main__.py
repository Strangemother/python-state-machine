'''
Import help for the examples.
'''

from os import listdir
from os.path import isfile, join, dirname, splitext

helpt= '''
The example files show basic operations and setups for scatter Nodes, Conditions
and Managers. Running an example

$ python -m scatter.examples.basic

$ python
>>> from scatter.examples import basic
>>> machine = basic.run()

--------------------------------------------------------------------------------

A List of provided examples:
'''
def allowed_file(f):
    '''
    Return bool if this file should be listed.
    '''
    not_pyc = splitext(f)[1] != '.pyc'
    not_prv = f.startswith('__') is False
    return not_pyc and not_prv

def sanatize(f):
    return splitext(f)[0]

def main():
    print helpt
    p = dirname(__file__)
    fls = [sanatize(f) for f in listdir(p) if isfile(join(p,f)) and allowed_file(f) ]

    print ', '.join(fls)


if __name__ == '__main__':
    main()
