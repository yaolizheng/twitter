import logging

log = logging.getLogger(__name__)


class Cache(object):

    def __init__(self, mc, prefix=None, limit=None):
        self.mc = mc
        self.prefix = prefix
        self.limit = limit

    def get_key(self, key):
        if self.prefix:
            return '%s-%s' % (self.prefix, key)
        else:
            return key

    def get(self, key):
        key = self.get_key(key)
        try:
            return self.mc[key]
        except KeyError:
            return None

    def set(self, key, value):
        self.mc[self.get_key(key)] = value

    def update(self, key, value):
        res = self.get(key)
        if res is not None:
            log.info('Update cache %s' % key)
            res.append(value)
            if self.limit is not None and len(res) > self.limit:
                res.pop(0)
            self.set(key, res)

    def remove(self, key, value):
        res = self.get(key)
        if res is not None:
            log.info('Remove cache %s' % key)
            res.remove(value)
            self.set(key, res)
