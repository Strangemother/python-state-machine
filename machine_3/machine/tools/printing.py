from termcolor import colored, cprint


def color_print(color, *args):
    t = [str(x) for x in args]
    s = ' '.join(t)
    cprint(s,color)
