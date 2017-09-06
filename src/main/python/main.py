#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import signal
import logging
from org.nmochizuki.decorators import exec_time
from org.nmochizuki.Controller import Controller
from configparser import ConfigParser

Pid = -1
logger = logging.getLogger(__name__)


def handler(signum, frame):
    """ signal handler """
    sys.stderr.write("Interrupted by the signal (mom)\n")
    sys.stderr.write("Killing pid %d\n" % (Pid,))
    sys.stderr.write("%s : %s\n" % (signum, frame,))

    os.kill(Pid, signal.SIGKILL)
    logger.info('killed pid: %d' % (Pid,))
    sys.exit(1)


@exec_time
def main():
    global Pid

    config = ConfigParser()
    config.read('src/main/config/default.ini')
    logging.basicConfig(
        level=eval(config['logging']['level']),
        format=config['logging']['format'],
        filename=config['logging']['path'])

    try:
        Pid = os.fork()
    except Exception as e:
        logger.error(e)
        return -1

    if Pid > 0:
        logger.info("pid : %d" % Pid)

    if Pid == -1:
        raise Exception("Failed to fork.")
    elif Pid == 0:
        controller = Controller()
        controller.execute()
    else:
        assert Pid > 0
        signal.signal(signal.SIGINT, handler)  # Ctrl-C
        signal.signal(signal.SIGTERM, handler)  # kill -term [PID]
        signal.signal(signal.SIGHUP, handler)  # kill -HUP [PID]
        signal.signal(signal.SIGQUIT, handler)  # Quit
        os.wait()

    return 0


if __name__ == "__main__":
    sys.exit(main())

