# -*- coding: utf-8 -*-
import sys
import logging
import inject
from argparse import ArgumentParser
from org.nmochizuki.validator import Validator
from org.nmochizuki.ExtExceptions import ValidatorError
from org.nmochizuki.module.Module import Module
from org.nmochizuki.module.AppModule import AppModule

class Controller(object):
    """ """
    module = None
    params = dict()
    logger = logging.getLogger(__name__)

    def __init__(self):
        """ """
        self.logger.info('Controller started.')
        self.parseArguments()

        try:
            Validator.valid(self.getParams())
        except ValidatorError as e:
            self.logger.error(e)
            sys.exit(-1)

        self.setModule(AppModule('benchmark', self.getParams()))

    def parseArguments(self):
        """ """
        parser = ArgumentParser()
        parser.add_argument('-u', '--url', required=True, type=str)
        parser.add_argument('-n', '--count', required=True, type=int)
        parser.add_argument('-c', '--worker', required=True, type=int)
        parser.add_argument('-q', '--qps', type=int)
        parser.add_argument('-m', '--method', type=int)
        args = parser.parse_args()

        self.params['url']    = args.url
        self.params['count']  = args.count
        self.params['worker'] = args.worker
        self.params['qps']    = args.qps
        self.params['method'] = args.method

    def setParams(self, params):
        self.params = params
        return self

    def setModule(self, module):
        self.module = module
        return self

    def getParams(self):
        return self.params

    def getModule(self):
        return self.module

    def execute(self):
        self.getModule().get().execute()

    def __del__(self):
        self.logger.info('Controller finished.')

