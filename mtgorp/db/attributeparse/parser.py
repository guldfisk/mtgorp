from abc import ABCMeta, abstractstaticmethod

class Parser(metaclass=ABCMeta):
	@abstractstaticmethod
	def parse(value):
		pass