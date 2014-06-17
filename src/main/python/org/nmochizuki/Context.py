# -*- coding: utf-8 -*-

class Context(object):
  """ interface """
  def bind(self, name, obj): raise NameError('Naming exception')
  def rebind(self, name, obj): raise NameError('Naming exception')
  def unbind(self, name): raise NameError('Naming exception')
  def rename(self, oldName, newName): raise NameError('Naming exception')

