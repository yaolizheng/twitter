import time
import datetime


class tweet:

    def __init__(self, id):
        self.id = id
        self.timestamp = time.time()

    def __repr__(self):
        return '(%s, %s)' % (self.id, datetime.datetime.utcfromtimestamp(self.timestamp))
