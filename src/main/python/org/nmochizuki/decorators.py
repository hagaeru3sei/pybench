# -*- coding: utf-8 -*-
import time
from threading import RLock

lock = RLock()


def synchronized(func):
    def _synchronized(*args, **kw):
        lock.acquire()
        with func(*args, **kw) as f:
            return f
    return _synchronized


def exec_time(func):
    """ 関数の実行時間を計測する.
    :param func:
    :return:
    """
    def _exec_time(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        r = time.time() - start
        print(r)
        return res
    return _exec_time
