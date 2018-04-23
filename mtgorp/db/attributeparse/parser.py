from abc import ABCMeta, abstractmethod

class Parser(metaclass=ABCMeta):

	@staticmethod
	@abstractmethod
	def parse(value):
		pass