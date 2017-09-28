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

class PreDash(BaseCardType):
	def __lt__(self, other):
		return ALL_TYPES_POSITION.get(self, -1) < ALL_TYPES_POSITION.get(other, -1)

class PostDash(BaseCardType):
	pass

class CardSuperType(PreDash):
	pass

class CardType(PreDash):
	pass

class CardSubType(PostDash):
	pass

SNOW = CardSuperType('Snow')
LEGENDARY = CardSuperType('Legendary')
WORLD = CardSuperType('World')
BASIC = CardSuperType('Basic')

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
	SEPARATOR = ' — '
	def __init__(self, types: t.Iterable[t.Union[CardSuperType, CardType]], sub_types: t.Iterable[CardSubType] = None):
		self._pre_dashes = types if isinstance(types, frozenset) else frozenset(types)
		self._post_dashes = (
			types if isinstance(sub_types, frozenset) else frozenset(sub_types)
		) if sub_types is not None else frozenset()
	def __eq__(self, other):
		return isinstance(other, CardTypes) and self._pre_dashes == other.types and self._post_dashes == other.sub_types
	def __hash__(self):
		return hash((self._pre_dashes, self._post_dashes))
	def __repr__(self):
		s = ' '.join(
			str(card_type)
			for card_type in
			sorted(self._pre_dashes)
		)
		if self._post_dashes:
			s += CardTypes.SEPARATOR + ' '.join(
				str(sub_type)
				for sub_type in
				sorted(self._post_dashes)
			)
		return s
	def __iter__(self):
		return itertools.chain(self._pre_dashes.__iter__(), self._post_dashes.__iter__())
	def __contains__(self, item):
		return item in self.__iter__()
	@property
	def super_types(self):
		return frozenset(t for t in self._pre_dashes if isinstance(t, CardSuperType))
	@property
	def card_types(self):
		return frozenset(t for t in self._pre_dashes if isinstance(t, CardType))
	@property
	def sub_types(self):
		return self._post_dashes

def test():
	ct = CardTypes(
		(BASIC, LAND, LEGENDARY),
		(CardSubType('Goat'), CardSubType('Human'), CardSubType('Angel'))
	)

	print(ct)

if __name__ == '__main__':
	test()