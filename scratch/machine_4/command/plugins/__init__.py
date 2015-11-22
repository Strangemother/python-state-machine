from pluginbase import PluginBase
import os
from functools import partial
from collections import namedtuple
from inspect import isclass, isfunction, ismethod


from cmd2 import options
from optparse import make_option


# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(here, '..')
get_path = partial(os.path.join, base_path)

_registered_plugins = []
RPlugin = namedtuple('RegisterPlugin', 'entity')
IPlugin = namedtuple('RegisterPlugin', 'entity, instance')


class Pluggable(object):

    name = 'Pluggable'

    def setup(self, name=None, paths=None):
        paths = paths or ['./plugins']
        self.plugin_base = PluginBase(package='plugins')
        self.setup_source(name)

    def setup_source(self, name):
        # and a source which loads the plugins from the "app_name/plugins"
        # folder.  We also pass the application name as identifier.  This
        # is optional but by doing this out plugins have consistent
        # internal module names which allows pickle to work.
        self.source = self.plugin_base.make_plugin_source(
            searchpath=[get_path('./plugins')],
            identifier=name)

    def import_plugin(self, name):
        '''
        Import a plugin by name
        '''
        return self.source.load_plugin(name)

    def register_load(self):
        '''
        Load the plugins, registering classes, modules and functions outside
        the plugin loader. Returned is a list of registered plugins.
        '''
        plugins = [x for x in self.source.list_plugins()]
        _s = 's' if len(plugins) != 1 else ''
        print 'setting up from {0} plugin location{1}'.format(len(plugins), _s)
        return self.load_plugins()

    def load_plugins(self):
        # Here we list all the plugins the source knows about, load them
        # and the use the "setup" function provided by the plugin to
        # initialize the plugin.
        plugins = self.source.list_plugins()
        for plugin_name in plugins:
            self.source.load_plugin(plugin_name)
        return _registered_plugins

    def register_iter(self):
        for plugin in _registered_plugins:
            yield plugin

    def create(self, app):
        '''
        iterate the plugins, instansiating each and proving a pointer
        '''
        for plugin in _registered_plugins:
            if hasattr(plugin, 'instance') is False:
                inst = self.create_instance(plugin)
                inst.app = app
                ri = IPlugin(plugin.entity, inst)
                _registered_plugins[_registered_plugins.index(plugin)] = ri

    def create_instance(self, plugin):
        '''
        Return an instance of a pluggable object based upon the
        entity provided.
        If a class is provided, it's assumed this is correctly foratted.
        IF a method is passed an instance of Plugin is generated with the
        name of the function as the command.
        '''
        if hasattr(plugin, 'entity') is False:
            import pdb; pdb.set_trace()  # breakpoint 1703bfb0 //

        entity = plugin.entity
        # print plugin
        if isclass(entity):
            inst = entity()
        elif isfunction(entity):
            inst = Plugin(entity.__name__, entity)
        else:
            inst = entity
            # get name
            # create plugin
        return inst

    def register_reduce(self, name, init_value):
        '''
        reduce the value through each name on the register list.
        returned is the value passed through all register methods defined
        by the name argument
        '''
        v = init_value

        for rplugin in self.register_iter():
            _v = getattr(rplugin.instance, name)(v)
            v = _v if _v is not None else v
        return v

    def generate_commands(self, app):
        '''
        Iterate each command, producing the correct methods to
        be implemented on the core object.
        '''
        gdo = []
        ghelp = []
        gcmpl = []

        for rplugin in self.register_iter():
            inst = rplugin.instance
            name, perf = self.generate_do_commands(app, inst)
            gdo.append(name)
            name, perf = self.generate_help_commands(app, inst)
            ghelp.append(name)
            name, perf = self.generate_complete_commands(app, inst)
            gcmpl.append(name)

        self.do_commands = gdo
        self.help_commands = ghelp
        self.complete_commands = gcmpl

    def generate_do_commands(self, app, inst):
        if hasattr(inst, 'perform'):
            # build attr
            name = inst.get_command_name()
            perf = partial(self.run_command, inst.perform, app)
            setattr(app, name, perf)
        return (name, perf)

    def generate_help_commands(self, app, inst):
        if hasattr(inst, 'help'):
            # build attr
            name = inst.get_help_name()
            perf = partial(self.run_help, inst.help, app)
            setattr(app, name, perf)
        return (name, perf)

    def generate_complete_commands(self, app, inst):
        if hasattr(inst, 'complete'):
            # build attr
            name = inst.get_complete_name()
            perf = partial(self.run_complete, inst.complete, app)
            setattr(app, name, perf)
        return (name, perf)

    def run_help(self, perform_method, app, *args):
        '''
        Run a help command
        '''
        help_str = None

        if isinstance(perform_method, (str, unicode)):
            help_str = perform_method
        elif ismethod(perform_method):
            help_str = perform_method(app)
        app._out(help_str)
        return help_str

    def run_command(self, perform_method, app, *args, **kw):
        '''
        run a command as handled by the app called by partial()
        providing the app as the first arg.
        '''
        v = perform_method(app, *args, **kw)
        if v is not None:
            app._out(v)
        return v

    def run_complete(self, perform_method, app, *args):
        ''''''
        v = perform_method(app, *args)
        if v is not None:
            app._out(v)
        return v

    def __getattr__(self, name):
        '''
        delegate to a reduce value through the plugins
        '''
        if hasattr(Plugin, name):
            return partial(self.register_reduce, name)
        else:
            raise AttributeError('{0} is not defined on Plugin'.format(name))


class PluginAPI(object):
    '''
    A default plugin structure of which can be implemented into the command
    line interface using the register_plugin method.
    '''


    '''
    String command defined for the command line. If this is None a lowercase
    form of the classe name is used by default
    '''
    command = None

    def get_command_name(self):
        return 'do_{0}'.format(self.get_name())

    def get_help_name(self):
        return 'help_{0}'.format(self.get_name())

    def get_complete_name(self):
        return 'complete_{0}'.format(self.get_name())

    def get_name(self):

        return self.name or self.command or self.__class__.__name__.lower()


class Plugin(PluginAPI):
    '''
    defined methods and fields to be used by an implementing plugin.
    '''

    app = None
    name = None
    help_str = None

    @staticmethod
    def callback(*args):
        pass

    def quit_app(self):
        return self.app.QUIT_EXIT

    def __init__(self, name=None, callback=None):
        self.name = name
        self.callback = staticmethod(callback)

    def perform(self, app, *args, **kw):
        '''
        perform the command. Arguments passed are command line arguments.
        '''
        if hasattr(self, 'callback') and hasattr(self.callback, '__func__'):
            # as static method call
            v = self.callback.__func__(*args, **kw)
            return v
        else:
            # run shell
            _a = [self.name]
            _a.extend(args)
            cmd = ' '.join(_a)
            return os.system(cmd)
        return None

    def setup(self):
        '''
        Perform a setup routine on your class. This is the filst method
        called by the implementor.
        '''
        pass

    def get_context(self, data):
        '''
        Return a context object
        '''
        return data

    def help(self, app):
        '''
        Return a string to print on the CLI as a help message
        '''

        if hasattr(self.callback, '__func__'):
            s = self.callback.__func__.__doc__
            if s is not None:
                return s
        return self.help_str or self.__class__.__doc__

    def complete(self, app, text, line, begidx, endidx):
        '''
        return a list of completion results for the provided
        string - this probably be a part string.
        '''
        return []


class _Plugin(Plugin):

    def __init__(self, **kw):
        self.__dict__.update(**kw)

    def get_self(self):
        return self

    entity = property(get_self)

def register_plugin(*args, **kw):
    '''
    Add a class registered plugin to the plugin set
    this will be called with the plugin library calls the
    file
    '''

    if len(kw.keys()) > 0:
        r = _Plugin(**kw)
    else:
        r = RPlugin(*args)
    _registered_plugins.append(r)
