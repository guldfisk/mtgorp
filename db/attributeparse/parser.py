from abc import ABCMeta, abstractstaticmethod

class Parser(metaclass=ABCMeta):
	@abstractstaticmethod
	def parse(s: str):
		pass