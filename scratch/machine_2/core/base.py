from blessings import Terminal

t = Terminal()

import logging

def logger():
    # create logger
    lgr = logging.getLogger('machine')
    lgr.setLevel(logging.DEBUG)
    # add a file handler
    fh = logging.FileHandler('machine.log')
    fh.setLevel(logging.WARNING)
    # create a formatter and set the formatter for the handler.
    frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(frmt)
    # add the Handler to the logger
    lgr.addHandler(fh)
    # You can now start issuing logging statements in your code
    lgr.debug('debug message') # This won't print to myapp.log
    lgr.info('info message') # Neither will this.
    lgr.warn('Checkout this warning.') # This will show up in the log file.
    lgr.error('An error goes here.') # and so will this.
    lgr.critical('Something critical happened.') # and this one too.
    return lgr

class Base(object):

    def log(self, *args, **kwargs):
        if kwargs.get('color') is None:
            if hasattr(self, 'log_color'):
                color = self.log_color
            else:
                color = 'white'
        else:
            color = kwargs.get('color')
        k = kwargs
        k['t'] = t
        s =  str('{t.%s}' % (color) + ' '.join([str(x) for x in args]) + '{t.normal}') .format(**k)
        # lgr.info(s)
        print s

