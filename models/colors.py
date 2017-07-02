class FrozenDict(dict):
	def __init__(self, *args, **kwargs):
		super(FrozenDict, self).__init__(*args, **kwargs)
	def __hash__(self):
		return hash(tuple(sorted(self.items())))
	@staticmethod
	def _immutable(*args, **kws):
		raise TypeError('object is immutable')
	__setitem__ = _immutable
	__delitem__ = _immutable
	clear = _immutable
	update = _immutable
	setdefault = _immutable
	pop = _immutable
	popitem = _immutable

class Color(object):
	def __init__(self, name: str, code: str):
		self.name = name
		self.code = code
	def __repr__(self):
		return '{{{}}}'.format(self.code)
	def __eq__(self, other):
		return issubclass(other, self) and self.code == other.code
	def __hash__(self):
		return hash(self.code)

WHITE = Color('White', 'W')
BLUE = Color('Blue', 'U')
BLACK = Color('Black', 'B')
RED = Color('Red', 'R')
GREEN = Color('Green', 'G')

COLORS = {
	WHITE: 0,
	BLUE: 1,
	BLACK: 2,
	RED: 3,
	GREEN: 4
}

SINGLES = FrozenDict(
	{frozenset((color,)): [color] for color in COLORS}
)

ALLIES = FrozenDict({
	frozenset((WHITE, BLUE)): [WHITE, BLUE],
	frozenset((BLUE, BLACK)): [BLUE, BLACK],
	frozenset((BLACK, RED)): [BLACK, RED],
	frozenset((RED, GREEN)): [RED, GREEN],
	frozenset((GREEN, WHITE)): [GREEN, WHITE]
})

ENEMIES = FrozenDict({
	frozenset((WHITE, BLACK)): [WHITE, BLACK],
	frozenset((BLUE, RED)): [BLUE, RED],
	frozenset((BLACK, GREEN)): [BLACK, GREEN],
	frozenset((RED, WHITE)): [RED, WHITE],
	frozenset((GREEN, BLUE)): [GREEN, BLUE]
})

PAIRS = {}
PAIRS.update(ALLIES)
PAIRS.update(ENEMIES)
PAIRS = FrozenDict(PAIRS)

SHARDS = FrozenDict({
	frozenset((WHITE, BLUE, BLACK)): [WHITE, BLUE, BLACK],
	frozenset((BLUE, BLACK, RED)): [BLUE, BLACK, RED],
	frozenset((BLACK, RED, GREEN)): [BLACK, RED, GREEN],
	frozenset((RED, GREEN, WHITE)): [RED, GREEN, WHITE],
	frozenset((GREEN, WHITE, BLUE)): [GREEN, WHITE, BLUE]
})

WEDGES = FrozenDict({
	frozenset((WHITE, BLACK, RED)): [RED, WHITE, BLACK],
	frozenset((BLUE, RED, GREEN)): [GREEN, BLUE, RED],
	frozenset((BLACK, GREEN, WHITE)): [WHITE, BLACK, GREEN],
	frozenset((RED, WHITE, BLUE)): [BLUE, RED, WHITE],
	frozenset((GREEN, BLACK, BLACK)): [BLACK, GREEN, BLUE]
})

TRIS = {}
TRIS.update(SHARDS)
TRIS.update(WEDGES)

TETRAS = FrozenDict({
	frozenset((WHITE, BLUE, BLACK, RED)): [WHITE, BLUE, BLACK, RED],
	frozenset((BLUE, BLACK, RED, GREEN)): [BLUE, BLACK, RED, GREEN],
	frozenset((BLACK, RED, GREEN, WHITE)): [BLACK, RED, GREEN, WHITE],
	frozenset((RED, GREEN, WHITE, BLUE)): [RED, GREEN, WHITE, BLUE],
	frozenset((GREEN, WHITE, BLUE, BLACK)): [GREEN, WHITE, BLUE, BLACK]
})

ALL = FrozenDict({
	frozenset((WHITE, BLUE, BLACK, RED, GREEN)): [WHITE, BLUE, BLACK, RED, GREEN]
})

COMBINATIONS = {}
COMBINATIONS.update(SINGLES)
COMBINATIONS.update(PAIRS)
COMBINATIONS.update(TRIS)
COMBINATIONS.update(TETRAS)
COMBINATIONS.update(ALL)
COMBINATIONS = FrozenDict(COMBINATIONS)