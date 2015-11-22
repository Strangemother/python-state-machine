from command.plugins import Plugin, register_plugin
import os


class Kill(Plugin):
    '''
    Standard kill command alike quit
    '''
    def perform(self, app, *args):
        return app.QUIT_NO_EXIT


class Plugins(Plugin):

    def perform(self, app, cmd):
        '''
        Perform plugin generations
        '''
        if cmd == 'load':
            self.app.generate_plugins()
        return cmd


class Clear(Plugin):

    def perform(self, app, cmd):
        '''
        Clear the screen
        '''
        app.onecmd('cls')

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def ls_complete(app, path, *args, **kw):
    p = path or app._cwd()
    app._out(args, path)
    mp = get_immediate_subdirectories(p)
    m = ['./{0}'.format(x) for x in mp]
    print mp, m
    return m

register_plugin(Plugins)
register_plugin(Kill)
register_plugin(Clear)
register_plugin(name='ls', complete=ls_complete)
