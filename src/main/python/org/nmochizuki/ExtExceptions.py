# -*- coding: utf-8 -*-
class ValidatorError(BaseException):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)
