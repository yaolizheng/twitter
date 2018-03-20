class MemcachedRetryException(Exception):

    def __init__(self, *args, **kwargs):
        super(MemcachedRetryException, self).__init__(*args, **kwargs)
        self.retry = True
