import typing as t
from enum import Enum


class Color(Enum):
	WHITE = 'W', 0
	BLUE = 'U', 1
	BLACK = 'B', 2
	RED = 'R', 3
	GREEN = 'G', 4
	
	@property
	def code(self):
		return '{{{}}}'.format(self._value)

	@property
	def letter_code(self):
		return self._value

	@property
	def position(self) -> int:
		return self._position

	def __lt__(self, other):
		return self.position < other.position
	
	def __new__(cls, code, position):
		obj = object.__new__(cls)
		obj._value = code
		obj._position = position
		return obj


AMOUNT_COLORS = 5


def color_set_sort_value(color_set: t.AbstractSet[Color]) -> int:
	return (
		sum(1 << c.position for c in color_set)
	)


def color_set_sort_value_len_first(color_set: t.AbstractSet[Color]) -> int:
	return (
		color_set_sort_value(color_set) << (AMOUNT_COLORS * len(color_set))
	)