import time
import datetime
import json
import logging

log = logging.getLogger(__name__)


class Timer(object):
    def __init__(self, name=None, duration=0, count=0):
        self.name = name
        self._starttime = None
        self._duration = duration
        self._count = count

    def start(self):
        self._starttime = time.time()

    def starttime(self):
        return self._starttime

    def stop(self, success):
        self._count += 1
        self._duration += time.time() - self._starttime
        self._starttime = None

    def wait(self, timeout):
        elapsed = self.seconds()
        if elapsed < timeout:
            time.sleep(timeout - elapsed)

    def remaining(self, period):
        elapsed = self.seconds()
        return max(0, period - elapsed)

    def seconds(self):
        elapsed = 0
        if self._starttime is not None:
            elapsed = time.time() - self._starttime
        return self._duration + elapsed

    def elapsed(self):
        return self.seconds()

    def __str__(self):
        return str(datetime.timedelta(seconds=self.seconds()))

    def result(self):
        return dict(
            length=str(datetime.timedelta(seconds=self.seconds())),
            count=self._count)

    def __repr__(self):
        return json.dumps(self.result(), indent=4)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            self.stop(False)
        else:
            self.stop(True)
        return False

    def __add__(self, other):
        duration = self._duration + other._duration
        count = self._count + other._count
        t = Timer(name=self.name, duration=duration, count=count)
        return t
