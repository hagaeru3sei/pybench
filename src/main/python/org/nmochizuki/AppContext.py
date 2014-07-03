# -*- coding: utf-8 -*-
import logging
from org.nmochizuki.Context import Context


class AppContext(Context):
    """ abstract """
    logger = logging.getLogger()

    def __init__(self):
        self.logger = logging.getLogger()
