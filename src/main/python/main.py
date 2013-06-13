#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import signal
import logging
from org.nmochizuki.Controller import Controller
from org.nmochizuki.module.AppModule import AppModule
from configparser import ConfigParser

Pid = -1
logger = logging.getLogger(__name__)

def handler(signum, frame):
    """ """
    sys.stderr.write("Interrupted by the signal (mom)\n")
    sys.stderr.write("Killing pid %d\n" % (Pid,))
    os.kill(Pid, signal.SIGKILL)
    logger.info('killed pid: %d' % (Pid,))
    sys.exit(1)

def main(*args, **kw):

    global Pid

    config = ConfigParser()
    config.read('src/main/config/default.ini')
    logging.basicConfig(
        level=eval(config['logging']['level']), 
        format=config['logging']['format'],
        filename=config['logging']['path'])

    try:
        Pid = os.fork()
        if Pid > 0:
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

    except Exception as e:
        logger.error(e)
        return -1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())

