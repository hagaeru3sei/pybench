# -*- coding: utf-8 -*-
from org.nmochizuki.ExtExceptions import ValidatorError


class Validator(object):
    def __init__(self):
        pass

    @classmethod
    def valid(cls, params):
        if not params['url']:
            raise ValidatorError('invalid url exception')
        if not params['count']:
            raise ValidatorError('invalid count exception')
        if not params['worker']:
            raise ValidatorError('invalid worker exception')

    def __del__(self):
        pass
