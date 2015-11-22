from command.plugins import Plugin, register_plugin
from cmd2 import options
from optparse import make_option


@options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
      make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
      make_option('-r', '--repeat', type="int", help="output [n] times")
     ])
def human(str_size, decimal_places=2, opts=None):
    '''
    Return a humanized string of the byte number provided.
    '''
    size = float(str_size)
    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
    UNITS = [B, KB, MB, GB, TB]
    df = "0%s.f" % (decimal_places)
    HUMANFMT = "%" + df + "%s"
    HUMANRADIX = 1024.
    dp = decimal_places
    for u in UNITS[:-1]:
        if size < HUMANRADIX : return HUMANFMT % (size, u)
        size /= HUMANRADIX

    return HUMANFMT % (dp, size, UNITS[-1])


register_plugin(human)
