import itertools

import typing as t

from abc import ABCMeta


class BaseCardType(metaclass=ABCMeta):
	def __init__(self, name: str):
		self._name = name
	@property
	def name(self):
		return self._name
	def __hash__(self):
		return hash((self.__class__, self._name))
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._name == other.name
	def __str__(self):
		return self._name
	def __lt__(self, other):
		return self._name < other.name

class SuperCardType(BaseCardType):
	pass

class CardType(BaseCardType):
	pass

class CardSubType(CardType):
	pass

SNOW = SuperCardType('Snow')
LEGENDARY = SuperCardType('Legendary')
WORLD = SuperCardType('World')
BASIC = SuperCardType('Basic')

SUPER_TYPES = (
	LEGENDARY,
	BASIC,
	WORLD,
	SNOW,
)

CREATURE = CardType('Creature')
ARTIFACT = CardType('Artifact')
ENCHANTMENT = CardType('Enchantment')
LAND = CardType('Land')
PLANESWALKER = CardType('Planeswalker')
INSTANT = CardType('Instant')
SORCERY = CardType('Sorcery')
TRIBAL = CardType('Tribal')

CARD_TYPES = (
	TRIBAL,
	ENCHANTMENT,
	ARTIFACT,
	LAND,
	CREATURE,
	PLANESWALKER,
	INSTANT,
	SORCERY
)

ALL_TYPES = SUPER_TYPES + CARD_TYPES

ALL_TYPES_POSITION = {
	t: idx for idx, t in enumerate(ALL_TYPES)
}

class CardTypes(object):
	separator = ' — '
	def __init__(self, types: t.Iterable[t.Union[SuperCardType, CardType]], sub_types: t.Iterable[CardSubType] = None):
		self.types = types if isinstance(types, frozenset) else frozenset(types)
		self.sub_types = (
			types if isinstance(sub_types, frozenset) else frozenset(sub_types)
		) if sub_types is not None else frozenset()
	def __eq__(self, other):
		return isinstance(other, CardTypes) and self.types == other.types and self.sub_types == other.sub_types
	def __hash__(self):
		return hash((self.types, self.sub_types))
	def __repr__(self):
		s = ' '.join(str(card_type) for card_type in sorted(self.types, key=lambda t: ALL_TYPES_POSITION.get(t, float('nan'))))
		if self.sub_types:
			s += CardTypes.separator + ' '.join(str(sub_type) for sub_type in sorted(self.sub_types))
		return s
	def __iter__(self):
		return itertools.chain(self.types.__iter__(), self.sub_types.__iter__())


def test():
	card_types = CardTypes(
		(BASIC, LAND),
		(CardSubType('Goat'), CardSubType('Human'))
	)

	print(card_types)


if __name__ == '__main__':
	test()