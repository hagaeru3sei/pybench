#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import signal
import logging
from org.nmochizuki.Controller import Controller
from configparser import ConfigParser

Pid = -1

def ttfb(func):
    import time
    def _ttfb(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        ttfb = time.time() - start
        print(ttfb)
        return res
    return _ttfb

def handler(signum, frame):
    """ """
    assert Pid > 0 
    print >> sys.stderr, "Interrupted by the signal (mom)"
    print >> sys.stderr, "Killing pid %d" % pid 
    os.kill(pid, signal.SIGKILL) #
    sys.exit(1)

def main(*args, **kw):

    global Pid

    config = ConfigParser()
    config.read('src/main/config/default.ini')
    logging.basicConfig(
        level=eval(config['logging']['level']), 
        format=config['logging']['format'],
        filename=config['logging']['path'])

    logger = logging.getLogger(__name__)

    try:
        Pid = os.fork()
        logger.info("pid : %d" % Pid)

        if Pid == -1:
            raise "Failed to fork."

        elif Pid == 0:
            controller = Controller()
            controller.execute()
        else:
            assert Pid > 0
            signal.signal(signal.SIGINT,  handler)  # Ctrl-c
            signal.signal(signal.SIGTERM, handler)  # Ctrl-
            signal.signal(signal.SIGHUP,  handler)  # Ctrl-
            signal.signal(signal.SIGQUIT, handler)  # Ctrl-
            os.wait()

        #while True:
        #    pass
            
    except Exception as e:
        logger.error(e)
        return -1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())

