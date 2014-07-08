# -*- coding: utf-8 -*-
import sys
import logging
from org.nmochizuki.variables import *
from org.nmochizuki.validator import Validator
from org.nmochizuki.ExtExceptions import ValidatorError
from org.nmochizuki.module.Module import Module
from org.nmochizuki.module.AppModule import AppModule
from argparse import ArgumentParser


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

            injector.binder.bind(AppName, "benchmark")
            injector.binder.bind(AppParams, self.getParams())

            self.setModule(injector.get(AppModule))

        except ValidatorError as e:
            self.logger.error(e)
            sys.exit(-1)

        except ImportError as e:
            self.logger.error(e)
            sys.exit(-1)

        except NameError as e:
            self.logger.error(e)
            sys.exit(-1)

    def parseArguments(self):
        """ """
        try:
            parser = injector.get(IArgumentParser)
        except Exception as e:
            self.logger.error(e)
            sys.exit(-1)

        parser.add_argument('-u', '--url', required=True, type=str)
        parser.add_argument('-n', '--count', required=True, type=int)
        parser.add_argument('-c', '--worker', required=True, type=int)
        parser.add_argument('-q', '--qps', type=int)
        parser.add_argument('-m', '--method', type=str)
        args = parser.parse_args()

        self.params['url'] = args.url
        self.params['count'] = args.count
        self.params['worker'] = args.worker
        self.params['qps'] = args.qps
        self.params['method'] = "GET"  # TODO:

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
