import time
import logging
from functools import wraps


log = logging.getLogger(__name__)


def has_retry_set(e):
    return bool(getattr(e, 'retry', None))


def always(e):
    return True


def retry(delay=1, timeout=None, iterations=0, on_exception=has_retry_set,
          exp_backoff=False):
    def make_wrapper(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.time()
            count = 1
            init_delay = delay
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    name = fn.__name__
                    duration = time.time() - start
                    count += 1
                    if exp_backoff:
                        init_delay *= 2
                    if timeout and duration > timeout:
                        logging.exception("Retrying %s timed out (%d seconds)"
                                          " timeout=%d",
                                          name, duration, timeout, exc_info=True)
                        raise
                    if iterations > 0 and count > iterations:
                        logging.exception(
                            "Retrying %s has reached iterations count",
                            name, exc_info=True)
                        raise
                    if on_exception(e):
                        logging.debug("Retrying %s in %s seconds",
                                      name, init_delay, exc_info=True)
                        time.sleep(init_delay)
                        if iterations > 0:
                            logging.debug("Retrying %s (%d of %d)",
                                          name, count, iterations,
                                          exc_info=True)
                        continue
                    else:
                        logging.exception("Not retrying %s",
                                          name, exc_info=True)
                        raise
        return wrapper
    return make_wrapper
