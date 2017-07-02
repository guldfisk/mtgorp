import typing as t
import multiset
import re

class CardType(str):
	pass

SNOW_SUPER_TYPE = CardType('Snow')
LEGENDARY_SUPER_TYPE = CardType('Legendary')
WORLD_SUPER_TYPE = CardType('World')
BASIC_SUPER_TYPE = CardType('Basic')

CREATURE_TYPE = CardType('Creature')
ARTIFACT_TYPE = CardType('Artifact')
ENCHANTMENT_TYPE = CardType('Enchantment')
LAND_TYPE = CardType('Land')
PLANESWALKER_TYPE = CardType('Planeswalker')
INSTANT_TYPE = CardType('Instant')
SORCERY_TYPE = CardType('Sorcery')
TRIBAL_TYPE = CardType('Tribal')

ALL_TYPES = (
	LEGENDARY_SUPER_TYPE,
	BASIC_SUPER_TYPE,
	WORLD_SUPER_TYPE,
	SNOW_SUPER_TYPE,
	TRIBAL_TYPE,
	ENCHANTMENT_TYPE,
	ARTIFACT_TYPE,
	LAND_TYPE,
	CREATURE_TYPE,
	PLANESWALKER_TYPE,
	INSTANT_TYPE,
	SORCERY_TYPE
)

ALL_TYPES_POSITION = {
	t: idx for idx, t in enumerate(ALL_TYPES)
}

class CardSubType(CardType):
	pass

class CardTypes(object):
	separator = ' — '
	def __init__(self, types: t.Iterable[CardType], sub_types: t.Iterable[CardSubType] = None):
		self.types = types if isinstance(types, multiset.FrozenMultiset) else multiset.FrozenMultiset(types)
		self.sub_types = (
			types if isinstance(sub_types, multiset.FrozenMultiset) else multiset.FrozenMultiset(sub_types)
		) if sub_types is not None else multiset.FrozenMultiset()
	def __eq__(self, other):
		return isinstance(other, CardTypes) and self.types == other.types and self.sub_types == other.sub_types
	def __hash__(self):
		return hash((self.types, self.sub_types))
	def __repr__(self):
		s = ' '.join(sorted(self.types, key=lambda t: ALL_TYPES_POSITION.get(t, float('nan'))))
		if self.sub_types:
			s += CardTypes.separator + ' '.join(sorted(self.sub_types))
		return s

class TypeParseException(Exception): pass

class Parser(object):
	super_type_matcher = re.compile('[^—]+')
	sub_type_matcher = re.compile('.*—(.*)')
	type_matcher = re.compile('\\w+')
	@staticmethod
	def parse(s: str) -> CardTypes:
		super_type_field = Parser.super_type_matcher.match(s)
		if not super_type_field:
			raise TypeParseException()
		super_types = (CardType(m.group()) for m in Parser.type_matcher.finditer(super_type_field.group()))
		sub_type_field = Parser.sub_type_matcher.match(s)
		sub_types = (
			CardSubType(m.group()) for m in Parser.type_matcher.finditer(sub_type_field.group(1))
		) if sub_type_field else ()
		return CardTypes(super_types, sub_types)


def test():
	card_types = CardTypes(
		(LEGENDARY_SUPER_TYPE, CREATURE_TYPE, ENCHANTMENT_TYPE, ARTIFACT_TYPE, SNOW_SUPER_TYPE),
		(CardSubType('Goat'), CardSubType('Human'))
	)
	parsed = Parser.parse('Legendary Enchantment Artifact Creature — Goat Human Ape')
	print(parsed)


if __name__ == '__main__':
	test()