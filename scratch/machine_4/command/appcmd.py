from cmd2 import Cmd
import os, sys
from plugins import Pluggable, Plugin
from cmd2 import options
from optparse import make_option

try:
    import readline
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
    readline.parse_and_bind('tab: complete')

PIPE = '|'

# Singals dected in the CMD loop to stop the app.
# Return from a calling method to kill the console.
QUIT_NO_EXIT = (False, -999)
QUIT_EXIT = (True, True)


# implement the plugins by calling the main`
# pluggable implementation and running the setup
_plugins = Pluggable()
_plugins.setup('command')


def main():
    '''
    Run the main application and start the command root.
    This is called from __main__
    '''
    app = App()
    app.cmdloop()


class AppBase(Cmd):
    '''
    Basic override and implementation of the Cmd2.Cmd
    class.
    '''

    _context = {}

    def parseline(self, line):
        '''
        Overrride the parse line, allowing the implementation
        of plugins to receive piped valus
        '''
        if '|' in line:
            self._out('piped', line)

        return Cmd.parseline(self, line)

    def invoke_args(self, callargs):
        '''
        Arguments passed to the invoke command.
        By default all arguments passed after the prompt
        file will be piped into the shell Cmd.
        '''
        return callargs

    def run_commands_at_invocation(self, callargs):
        '''
        override the method to slice the first arument adding the
        'invoke_args' method
        '''
        cargs = self.invoke_args(callargs)
        for initial_command in cargs:
            if self.onecmd_plus_hooks(initial_command + '\n'):
                return self._STOP_AND_EXIT

    def context(self, obj):
        '''
        provide a context object for the application scope to receive
        for command line implementation
        '''
        self._context.update(obj)

    def do_pipe(self, args):
        buffer = None
        for arg in args:
            s = arg
            if buffer:
                # This command just adds the output of a previous command as the last argument
                s += ' ' + buffer
            self.onecmd(s)
            buffer = self.output

    def _pre(self, *args):
        '''
        Called prior to a line
        '''
        print 'pre', args

    def complete(self, text, line):

        return self._complete(text, line)

    def _complete(self, text, state):
    # def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """

        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            if self.completion_matches is not None:
                return self.completion_matches[state]
        except IndexError:
            return None


    def completedefault(self, text, line, begidx, endidx):
        '''
        Return the file directory list
        '''
        self._out('\nDefault completion', text)


    def _post(self, *args):
        '''
        Called after a command
        '''
        # print 'post', args
        pass

    def _cwd(self):
        '''
        Return the current working directory string
        '''
        return os.path.dirname(os.path.realpath(__file__))

    def do_context(self, obj):
        '''
        return context object
        '''
        self._out('perform context', self._lastcmd)

    def create_root_command(self, obj):
        '''
        convert each object to a callable command to read and set
        '''
        for k in obj:
            n = 'do_{0}'.format(k)
            setattr(self, n, self.do_context)

        self.generate_plugins()

    def generate_plugins(self):
        '''
        Run the plugin generator ensing plugins are ready to call
        '''
        _plugins.generate_commands(self)

    def _change_dir(self, path):
        '''
        Provide a path to alter the python current working DIR. this is
        called on the command line as 'cd'
        '''
        os.chdir(path)
        p =  self._cwd()
        self._out('cwd', p)
        return p

    def create_root(self, *args):
        '''
        Build the root area prior to command loop start
        '''
        ctx = _plugins.get_context(self._context)
        readline.set_completer(self._complete)
        readline.parse_and_bind(self.completekey+": complete")

        if ctx is not None:
            # print 'creating root', ctx.keys()
            self.create_root_command(ctx)

    def set_prompt(self, line):
        '''
        Change the prompt of the Cli
        '''
        self.prompt = '{0}> '.format(line)
        return self.prompt


class CmdApp(AppBase):
    '''
    Interface application class designed to override and interface with the Cmd
    class and communicate from App paret class.
    '''
    # customized attributes and methods here
    prompt = '> '
    intro = 'App Commander v0.1'
    default_to_shell = True

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        '''
        Initialize the CmdApp performing a load of the plugins and
        passing the arguments to the super.
        '''
        _plugins.register_load()
        return AppBase.__init__(self, completekey, stdin, stdout)

    def _out(self, *args):
        '''
        Send the arguments provided to the feedback of the CLI.
        This allows ... arguments of which will be converted to str()
        '''
        s = ' '.join([str(x) for x in args])
        self.pfeedback(s)

    def default(self, arg):
        '''
        Default output if a command does not exist.
        '''
        self._out('{0} does not exist'.format(arg))

    def get_names(self):
        '''
        Return the names associated with the help,
        add the plugins helps as setattr doesn't load into
        __class__ of which the do_help leverages.
        '''
        return dir(self)

    def precmd(self, *args):
        '''
        call the hook _pre and delegate to plugins
        '''
        self._pre(*args)
        return Cmd.precmd(self, *args)

    def postcmd(self, *args):
        '''
        call the hook _post and delegate to plugins
        '''
        self._post(*args)
        return Cmd.postcmd(self, *args)

    def preloop(self, *args):
        '''
        Add the context object to the command line scope
        '''
        _plugins.create(self)
        self.create_root(*args)

        self.set_prompt(self._cwd())
        return Cmd.preloop(self, *args)

    def onecmd_plus_hooks(self, line, return_none=True):
        '''
        A single command called with the addtional options provided
        to configure the method call.
        Returned is the value from the Piped reduce call
        or the handler method.
        '''
        # print 'onecmd_plus_hooks', line
        self._lastcmd = line
        if PIPE in line:
            spl = line.split(PIPE)
            return self.run_commands_reduce(spl)
        else:
            v = Cmd.onecmd_plus_hooks(self, line)

            to_quit = False
            if v in (QUIT_EXIT, QUIT_NO_EXIT):
                to_quit = True
            if return_none is False or to_quit:
                return v

    def run_commands_reduce(self, cmds):
        '''
        Perform each command, passing the return value in the next
        function right to left.
        >>> size . | human
        '''
        v = None

        for _cmd in cmds:
            cmd_v = _cmd
            # print 'read', cmd_v
            if v is not None:
                cmd_v = '{0} {1}'.format(_cmd, v)
            v = self.onecmd_plus_hooks(cmd_v, return_none=False)
            if v is None:
                self._out('{0} broke pattern'.format(cmd_v))


class CmdAppCommands(CmdApp):

    def do_quit(self, arg):
        '''
        Return the Quit signal.
        '''
        return QUIT_EXIT

    def do_EOF(self, line):
        '''
        Return the Quit signal
        '''
        return QUIT_EXIT

    do_exit = do_quit
    do_q = do_quit

    def do_cwd(self, arg):
        '''
        prints the current working directory
        '''
        c = self._cwd()
        self._out(c)

    def do_cd(self, arg):
        '''
        Change the current working directory
        '''
        c = self._change_dir(arg)
        self.set_prompt(c)

    def do_stat(self, path=None):
        '''
        get the statistics of a given directory. Default cwd
        '''
        path = path or self._cwd()
        stat = os.stat(path)
        self._out(stat)


App = CmdAppCommands


if __name__ == '__main__':
    main()
