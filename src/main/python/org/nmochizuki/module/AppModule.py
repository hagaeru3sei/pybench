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

  name   = ""
  params = dict()
  app  = None
  module = None
  logger = logging.getLogger(__name__)

  @inject(name=AppName, params=AppParams)
  def __init__(self, name, params):
    """ Override Module.__init__ """
    self.setName(name).setParams(params)

    try:
      self.setApp(eval(name[0].upper() + name[1:]))
      self.setModule(eval(name[0].upper() + name[1:] + "Module"))

    except NameError as e:
      self.logger.error(e)
      sys.exit(-1)

  def getModule(self):
    return self.module

  def getApp(self):
    return self.app

  def getName(self):
    return self.name

  def getParams(self):
    return self.params

  def setApp(self, app):
    self.app = app
    return self

  def setModule(self, module):
    self.module = module
    return self

  def setName(self, name):
    self.name   = name
    return self

  def setParams(self, params):
    self.params = params
    return self

  def get(self):
    return self.app(self.getModule(), self.getParams())


