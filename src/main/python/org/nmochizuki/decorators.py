# -*- coding: utf-8 -*-
import time
from threading import RLock
lock = RLock()
def synchronized(function):
    def _synchronized(*args, **kw):
        lock.acquire()
        with function(*args, **kw) as func:
            return func
    return _synchronized

def ttfb(func):
    def _ttfb(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        ttfb = time.time() - start
        print(ttfb)
        return res
    return _ttfb


