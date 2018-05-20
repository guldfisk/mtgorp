import typing as t


class PTValue(object):
	
	def __init__(self, value: int=0, variable: bool=False):
		self._value = value
		self._variable = variable
	
	@property
	def value(self) -> int:
		return 0 if self._variable else self._value
	
	@property
	def variable(self) -> bool:
		return self._variable
	
	def __str__(self):
		return '*' if self._variable else str(self._value)
	
	def __eq__(self, other):
		return (
			isinstance(other, int) and self.value == other
			or isinstance(other, self.__class__) and self.value == other.value
		)
	
	def __lt__(self, other):
		return (
			isinstance(other, int) and self.value < other
			or isinstance(other, self.__class__) and self.value == other.value
		)
	
	def __le__(self, other):
		return (
			isinstance(other, int) and self.value <= other
			or isinstance(other, self.__class__) and self.value == other.value
		)
	
	def __gt__(self, other):
		return (
			isinstance(other, int) and self.value > other
			or isinstance(other, self.__class__) and self.value == other.value
		)
	
	def __ge__(self, other):
		return (
			isinstance(other, int) and self.value >= other
			or isinstance(other, self.__class__) and self.value == other.value
		)


class PowerToughness(object):
	
	def __init__(self, power: t.Union[int, PTValue], toughness: t.Union[int, PTValue]):
		self._power = power if isinstance(power, PTValue) else PTValue(power)
		self._toughness = toughness if isinstance(toughness, PTValue) else PTValue(toughness)
	
	@property
	def power(self) -> PTValue:
		return self._power
	
	@property
	def toughness(self) -> PTValue:
		return self._toughness
	
	def __eq__(self, other):
		return (
			isinstance(other, PowerToughness)
			and self.power == other.power
			and self.toughness == other.toughness
		)
	
	def __hash__(self):
		return hash((self.power, self.toughness))
	
	def __repr__(self):
		return '{}/{}'.format(self.power, self.toughness)
	
	def __iter__(self):
		yield self.power
		yield self.toughness
