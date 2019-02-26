import time


class Retry(object):
    def __init__(self, max_retries=3, wait=0, exceptions=(Exception,)):
        self.max_retries = max_retries
        self.exceptions = exceptions
        self.wait = wait

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for i in range(self.max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                except self.exceptions:
                    time.sleep(self.wait)
                    continue
                else:
                    return result
        return wrapper