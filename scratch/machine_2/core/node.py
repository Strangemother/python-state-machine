from base import Base
import inspect

class Conditions(object):
    '''
    A Mixin construct to assist in applying and managing conditions.
    '''

    def conditions(self):
        '''
        Returns a list of conditions to meet.
        '''
        return ()


class GetSetMixin(object):
    '''
    Provide a entry point for monitoring the change in
    the mointored variables.
    '''

    def watch(self, node, names):
        '''
        Provide a node and a list of variables to monitor.
        '''
        for name in names:
            self.monitor_key(node, name)


    def monitor_key(self, node, name):
        '''
        watch events to changes of the supplied named key 
        on the provided node. 
        ''' 
        def delx(self):
            print "+++ delx()"
            # del self.__x
        
        def proxy_get(self, k):
            print 'proxy get', k 

        def proxy_set(self, k):
            print 'proxy set', k 
        
        print 'monitor', name


    def get(self, k): 
        '''
        return an attribute from this node
        '''
        print 'get', k
        return getattr(self, k)

    def set(self, k, v):
        '''
        Change an attribute on this node
        '''
        # import pdb;pdb.set_trace()
        setattr(self, k, v)
        return self.get(k)


class NodeBase(Base, GetSetMixin):
    # A must-have field
    #
    name = None

    def is_valid(self):
        '''
        returns boolean if the node conditions have been fully met.
        '''
        return True

    def valid(self):
        '''
        All conditions have been met. This node is valid. 
        The valid state may change when the network alters.
        '''
        pass


    def get_attrs(self):
        '''
        return the fields for this nbode to be associated on the network.
        These are attributes and methods supplied to the class
        '''
        ignore = Node.__dict__.keys()
        # ignore = reduce(lambda x, y: x+y, [x.__dict__.keys() for x in iter(classes)])
        fields = []
        classes = self.__class__.__mro__
        # rint classes
        for parent_class in iter(classes):
            # print 'class', parent_class
            keys = parent_class.__dict__.keys()
            ckeys = self.__class__.__dict__.keys()
            for model_field in keys:
                is_cls = inspect.isclass(getattr(parent_class, model_field))
                is_meta = model_field == 'Meta' and is_cls
                name = model_field
                if is_meta or model_field in ignore or model_field.startswith('__'):
                    continue
                if model_field in ckeys:
                    fields.append(name)

        for field in ignore:
            name = field
            if field in ignore or field.startswith('__'):
                continue
            ignore.append(name)
        return fields

    def __setitem__(self, k, v):
        return self.set(k, v)

    def __getitem__(self, k):
        return self.get(k)


class Node(NodeBase, Conditions):
    '''
    Exposed api for integration to the network
    '''
     
    def __setattr__(self, name, value):
        print "Setting", name
        super(Node, self).__setattr__(name, value)

    def __getattr__(self, name):
        print 'get', name
        return super(Node, self).__getattr__(name)


class TestNode(Node):
    color = 'red'
    age = 22
    food = 'cherry'
    bar = 2
