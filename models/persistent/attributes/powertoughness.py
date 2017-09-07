import re
import typing as t

from managejson.attributeparse.exceptions import AttributeParseException


class PTValue(object):
	def __init__(self, value: int=0, variable: bool=False):
		self._value = value
		self._variable = variable
	@property
	def value(self):
		return 0 if self._variable else self._value
	@property
	def variable(self):
		return self._variable
	def __str__(self):
		return '*' if self._variable else str(self._value)
	def __eq__(self, other):
		return self.value == other
	def __lt__(self, other):
		return self.value < other
	def __le__(self, other):
		return self.value <= other
	def __gt__(self, other):
		return self.value > other
	def __ge__(self, other):
		return self.value >= other

class PowerToughness(object):
	def __init__(self, power: t.Union[int, PTValue], toughness: t.Union[int, PTValue]):
		self._power = power if isinstance(power, PTValue) else PTValue(power)
		self._toughness = toughness if isinstance(toughness, PTValue) else PTValue(toughness)
	@property
	def power(self):
		return self._power
	@property
	def toughness(self):
		return self._toughness
	def __eq__(self, other):
		return isinstance(other, PowerToughness) and self.power == other.power and self.toughness == other.toughness
	def __hash__(self):
		return hash((self.power, self.toughness))
	def __repr__(self):
		return '{}/{}'.format(self.power, self.toughness)
	def __iter__(self):
		yield self.power
		yield self.toughness

def test():
	pass
	# pt = Parser.parse_string('12/-23*')
	#
	# print(pt)

if __name__ == '__main__':
	test()