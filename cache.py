import logging
import retry
from exception import MemcachedRetryException

log = logging.getLogger(__name__)


class Cache(object):

    """
    Client module for memcached.
    """

    def __init__(self, mc, prefix=None, limit=None, dup=True):
        self.mc = mc
        self.prefix = prefix
        self.limit = limit
        self.dup = dup

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

    def cas(self, key, value, token):
        return self.mc.cas(key, value, token)

    def gets(self, key):
        return self.mc.gets(key)

    @retry.retry(timeout=10)
    def update(self, key, value):
        """
        Function to add value to existing key.
        """
        key = self.get_key(key)
        res, token = self.gets(key)
        if res is not None:
            log.info('Update cache %s' % key)
            if not self.dup:
                if value not in res:
                    res.append(value)
            else:
                res.append(value)
            if self.limit is not None and len(res) > self.limit:
                res.pop(0)
            if not self.cas(key, res, token):
                raise MemcachedRetryException()

    @retry.retry(timeout=10)
    def remove(self, key, value):
        """
        Function to remove value for existing key.
        """
        key = self.get_key(key)
        res, token = self.gets(key)
        if res is not None:
            log.info('Remove cache %s' % key)
            if value in res:
                res.remove(value)
                if not self.cas(key, res, token):
                    raise MemcachedRetryException()

    def delete(self, key):
        try:
            key = self.get_key(key)
            del self.mc[key]
        except KeyError:
            return None
        except:
            log.exception('Failed to delete key %s' % key)
