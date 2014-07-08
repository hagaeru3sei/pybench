# -*- coding: utf-8 -*-
import logging
import sys

from org.nmochizuki.variables import *
from injector import inject
from org.nmochizuki.module.Benchmark import Benchmark
from org.nmochizuki.module.Benchmark import BenchmarkModule
from org.nmochizuki.module.Module import Module
from org.nmochizuki.AppContext import AppContext


class AppModule(Module):
    name = ""
    params = dict()
    app = None
    module = None
    logger = logging.getLogger(__name__)

    @inject(name=AppName, params=AppParams)
    def __init__(self, name, params):
        """ Override Module.__init__ """
        super().__init__(name, params)

        try:
            self.setApp(eval(name[0].upper() + name[1:]))
            self.setModule(eval(name[0].upper() + name[1:] + "Module"))

        except NameError as e:
            self.logger.error(e)
            sys.exit(-1)

    def getModule(self) -> Module:
        return self.module

    def getApp(self) -> AppContext:
        return self.app

    def getName(self) -> str:
        return self.name

    def getParams(self) -> dict:
        return self.params

    def setApp(self, app):
        self.app = app
        return self

    def setModule(self, module):
        self.module = module
        return self

    def setName(self, name):
        self.name = name
        return self

    def setParams(self, params):
        self.params = params
        return self

    def get(self) -> AppContext:
        return self.app(self.getModule(), self.getParams())
