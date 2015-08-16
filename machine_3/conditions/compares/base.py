class CacheMixin(object):
    '''
    Tools to analyse direction of change for a given conditional.
    '''

    def store(self, field=None, nodes=None):
        '''
        store the cache for change analysis upon next iteration.
        '''
        field = field or getattr(self, 'field')
        nodes = nodes or getattr(self, 'get_nodes')()

        if field is None or nodes is None:
            return False

        __cache = self._get_cache()

        if __cache.has_key(field) is not True:
            __cache[field] = []

        cnt=0

        for node in nodes:
            written = self._write_cache(node, field)
            if written:
                cnt += 1

        self._set_cache(__cache)
        return len(nodes) == cnt

    def _get_cache(self):
        '''
        return a dict for use as a cache object
        A new self.__cache = {} will be created if it
        does not exist
        '''

        if hasattr(self, '__cache') is not True:
            self.__dict__['__cache'] = {}

        __cache = getattr(self,'__cache')
        return __cache

    def _has_cache(self):
        return hasattr(self, '__cache')

    def _write_cache(self, node, field):
        __cache = self._get_cache()
        try:
            # original value
            v = getattr(node, field)
        except AttributeError as e:
            return False
        # original length
        l = len(__cache[field])
        # push value
        __cache[field].append(v)
        ll = len(__cache[field])
        return (ll - 1) == l

    def _set_cache(self, __cache):
        '''
        write an object as the cache dict.
        '''
        setattr(self, '__cache', __cache)

    def store_cache(self, key, level=-1):
        '''
        return the cached store of the provided key
        by default the last in is provided `level=-1`
        '''
        __cache = self._get_cache()

        v = __cache[key] if __cache.has_key(key) else None
        if v is not None:
            return v[level]
        return False


class Compare(object):

    def __init__(self, condition=None):
        self.condition = condition

    def match(self, a, b):
        return a == b


class CacheCompare(Compare, CacheMixin):
    '''
    A cache value is stored to compare against
    '''
    def match(self, a, b):
        v = super(CacheCompare, self).match(a, b)
        self.store(a)
        return v
