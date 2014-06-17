# -*- coding: utf-8 -*-
from injector import Key
from injector import Injector
from argparse import ArgumentParser

# DI
injector        = Injector()
IArgumentParser = Key('IArgumentParser')
AppName         = Key('AppName')
AppParams       = Key('AppParams')
injector.binder.bind(IArgumentParser, ArgumentParser)

if AppName and AppParams:
  from org.nmochizuki.module.AppModule import AppModule

injector.binder.bind(AppModule)

