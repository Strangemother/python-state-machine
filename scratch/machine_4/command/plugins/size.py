from command.plugins import Plugin, register_plugin
from cmd2 import options
from optparse import make_option
import shlex
import os, argparse


def get_size(start_path='.'):
    total_size = 0
    seen = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                stat = os.stat(fp)
            except OSError:
                continue

            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue

            total_size += stat.st_size

    return total_size


def _total_size(source):
    '''
    Recursively decend the source children to determine the true size of a
    folder's files. Retuned is an int of total bytes
    '''
    total_size = os.path.getsize(source)
    for item in os.listdir(source):
        itempath = os.path.join(source, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += _total_size(itempath)
    return total_size


parser = argparse.ArgumentParser()
parser.add_argument('--foo', action='store_true')
parser.add_argument('--bar', action='store_false')
parser.add_argument('--baz', action='store_false')


class Size(Plugin):
    '''
    Inline help message
    '''
    command = 'size'
    parser = None

    def __init__(self):
        self.parse = parser

    def get_context(self, data):
        data['size'] = 'foo'
        return data

    def parse_switches(self, string):
        '''
        Parse and return the value passed from the command line to
        the perform method - returned is a namedspace from the arg parser
        and the unparsed remaining values from the string.
        '''
        spl = shlex.split(string)
        switches, unparsed = parser.parse_known_args(spl)
        return (unparsed, switches)

    def complete(self, app, text, line, begidx, endidx):
        # self.app._out('size complete', text)
        return ['foo']

    def perform(self, app=None, line=None, *args,  **kw):
        '''
        print the size of the provided file or folder
        '''
        paths, sw = self.parse_switches(line)
        size = 0
        for path in paths:
            path = str(path or app._cwd())
            try:
                v = _total_size(path)
            except:
                v = 0
            if isinstance(v, (int, float,long)):
                size += v
        return size

    def help(self, app):
        return self.perform.__doc__


register_plugin(Size)
