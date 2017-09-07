import typing as t
from enum import Enum

class Color(Enum):
	WHITE = 'W'
	BLUE = 'U'
	BLACK = 'B'
	RED = 'R'
	GREEN = 'G'
	@property
	def code(self):
		return '{{{}}}'.format(self.value)
	def __lt__(self, other):
		return COLOR_VALUES[self] < COLOR_VALUES[other]

AMOUNT_COLORS = len(tuple(Color))

COLOR_VALUES = {
	c: i+1 for i, c in enumerate(Color)
}

COLOR_VALUES_INVERSE = {
	c: AMOUNT_COLORS-i+1 for i, c in enumerate(Color)
}

def color_set_sort_value(color_set: t.AbstractSet[Color]):
	return (
		sum(1<<COLOR_VALUES[c] for c in color_set)
	)

def test():
	print(Color.GREEN < Color.RED)

if __name__ == '__main__':
	test()