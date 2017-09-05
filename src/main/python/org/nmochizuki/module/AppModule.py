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

    @inject
    def __init__(self, name: AppName, params: AppParams):
        """ Override Module.__init__ """
        super().__init__(name, params)

        try:
            self.set_app(eval(name[0].upper() + name[1:]))
            self.set_module(eval(name[0].upper() + name[1:] + "Module"))

        except NameError as e:
            self.logger.error(e)
            sys.exit(-1)

    def get_module(self) -> Module:
        return self.module

    def get_app(self) -> AppContext:
        return self.app

    def get_name(self) -> str:
        return self.name

    def get_params(self) -> dict:
        return self.params

    def set_app(self, app):
        self.app = app
        return self

    def set_module(self, module):
        self.module = module
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_params(self, params):
        self.params = params
        return self

    def get(self) -> AppContext:
        return self.app(self.get_module(), self.get_params())
