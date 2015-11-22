try:
    from colorama import init
    module_colorama = True
except ImportError:
    module_colorama = False

try:
    from termcolor import cprint
    module_termcolor = True
except ImportError:
    module_termcolor = False

if module_colorama is not False:
    init()


def color_print(color, *args):
    t = [str(x) for x in args]
    s = ' '.join(t)
    if module_termcolor is not False:
        cprint(s, color)
    else:
        print s
