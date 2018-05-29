import typing as t

from abc import ABCMeta, abstractmethod

from mtgorp.models.interfaces import Cardboard, Printing, Expansion, Block

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flags
from mtgorp.models.persistent.attributes.typeline import TypeLine
from mtgorp.models.persistent.attributes.manacosts import ManaCost
from mtgorp.models.persistent.attributes.powertoughness import PTValue


searchable = t.Union[Cardboard, Printing]


class Extractor(object, metaclass=ABCMeta):
	extraction_type = None #type: t.Type

	@staticmethod
	@abstractmethod
	def extract(model: searchable) -> t.Iterable[t.Any]:
		pass


class PrintingNameExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[str]:
		return printing.cardboard.name.lower(),


class CardboardNameExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[str]:
		return cardboard.name.lower(),


class PrintingLayoutExtractor(Extractor):
	extraction_type = Layout

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[Layout]:
		return printing.cardboard.layout,


class CardboardLayoutExtractor(Extractor):
	extraction_type = Layout

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[Layout]:
		return cardboard.layout,


class PrintingCMCExtractor(Extractor):
	extraction_type = int

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[int]:
		return (card.cmc for card in printing.cardboard.cards)


class CardboardCMCExtractor(Extractor):
	extraction_type = int

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[int]:
		return (card.cmc for card in cardboard.cards)


class PrintingRarityExtractor(Extractor):
	extraction_type = Rarity

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[Rarity]:
		return printing.rarity,


class CardboardRarityExtractor(Extractor):
	extraction_type = Rarity

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[Rarity]:
		return (printing.rarity for printing in cardboard.printings)


class PrintingFlagsExtractor(Extractor):
	extraction_type = Flags

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[Flags]:
		return printing.flags,


class CardboardFlagsExtractor(Extractor):
	extraction_type = Flags

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[Flags]:
		return (printing.flags for printing in cardboard.printings)


class PrintingTypesExtractor(Extractor):
	extraction_type = TypeLine

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[TypeLine]:
		return (card.type_line for card in printing.cardboard.cards)


class CardboardTypesExtractor(Extractor):
	extraction_type = TypeLine

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[TypeLine]:
		return (card.type_line for card in cardboard.cards)


class PrintingManaCostExtractor(Extractor):
	extraction_type = ManaCost

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[ManaCost]:
		return (card.mana_cost for card in printing.cardboard.cards)


class CardboardManaCostExtractor(Extractor):
	extraction_type = ManaCost

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[ManaCost]:
		return (card.mana_cost for card in cardboard.cards)


class PrintingOracleExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[str]:
		return (card.oracle_text.lower() for card in printing.cardboard.cards)


class CardboardOracleExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[str]:
		return (card.oracle_text.lower() for card in cardboard.cards)


class PrintingFlavorExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Optional[str]]:
		return (face.flavor for face in printing.faces)


class CardboardFlavorExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Optional[str]]:
		return (face.flavor for printing in cardboard.printings for face in printing.faces)


class PrintingPowerExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Optional[PTValue]]:
		return (
			card.power_toughness.power
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)


class CardboardPowerExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Optional[PTValue]]:
		return (
			card.power_toughness.power
			if card.power_toughness is not None else
			None
			for card in
			cardboard.cards
		)


class PrintingToughnessExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Optional[PTValue]]:
		return (
			card.power_toughness.toughness
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)


class CardboardToughnessExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Optional[PTValue]]:
		return (
			card.power_toughness.toughness
			if card.power_toughness is not None else
			None
			for card in
			cardboard.cards
		)


class PrintingLoyaltyExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Optional[PTValue]]:
		return (card.loyalty for card in printing.cardboard.cards)


class CardboardLoyaltyExtractor(Extractor):
	extraction_type = PTValue

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Optional[PTValue]]:
		return (card.loyalty for card in cardboard.cards)


class PrintingArtistExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[str]:
		return (
			None
			if face.artist is None else
			face.artist.name.lower()
			for face in
			printing.faces
		)


class CardboardArtistExtractor(Extractor):
	extraction_type = str

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[str]:
		return (
			None
			if face.artist is None else
			face.artist.name.lower()
			for printing in
			cardboard.printings
			for face in
			printing.faces
		)


class PrintingExpansionExtractor(Extractor):
	extraction_type = Expansion

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[Expansion]:
		return printing.expansion,


class CardboardExpansionExtractor(Extractor):
	extraction_type = Expansion

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[Expansion]:
		return (printing.expansion for printing in cardboard.printings)


class PrintingBlockExtractor(Extractor):
	extraction_type = Block

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[Block]:
		return None if printing.expansion is None else printing.expansion.block,


class CardboardBlockExtractor(Extractor):
	extraction_type = Block

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[Block]:
		return (
			None
			if printing.expansion is None else
			printing.expansion.block
			for printing in
			cardboard.printings
		)


class Matchable(object):

	@abstractmethod
	def match(self, model: searchable) -> bool:
		pass

	def __call__(self, model) -> bool:
		pass


class AttributeMatch(Matchable, metaclass=ABCMeta):

	def __init__(self, extractor: t.Type[Extractor], value: t.Union[t.Type[Extractor], t.Any]):
		self._extractor = extractor
		self._value = value
		self.__check = (
			self._check_value_is_extractor
			if isinstance(value, type) else
			self._check_value
		)

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__
			and self._extractor == other._extractor
			and self._value == other._value
		)

	def __hash__(self):
		return hash((self.__class__, self._extractor, self._value))

	def match(self, model: searchable) -> bool:
		return any(
			extracted is not None and self.__check(extracted, model)
			for extracted in
			self._extractor.extract(model)
		)

	def __check(self, remote, model: searchable) -> bool:
		pass

	def _check_value(self, remote, model: searchable) -> bool:
		return self._check(self._value, remote)

	def _check_value_is_extractor(self, remote, model: searchable) -> bool:
		return any(
			extracted is not None
			and self._check(extracted, remote)
			for extracted in
			self._value.extract(model)
		)

	@classmethod
	@abstractmethod
	def _check(cls, own, remote) -> bool:
		pass

	def __repr__(self) -> str:
		return '{}({}, {})'.format(
			self.__class__.__name__,
			self._extractor.__name__,
			(
				self._value.__name__
				if isinstance(self._value, type) else
				self._value
			),
		)


class Equals(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return own == remote


class GreaterThan(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return remote > own


class GreaterThanOrEquals(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return remote >= own


class LessThan(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return remote < own


class LessThanOrEquals(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return remote <= own


class Contains(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return own in remote


class ContainedIn(AttributeMatch):

	@classmethod
	def _check(cls, own, remote) -> bool:
		return remote in own


class 	Pattern(Matchable, metaclass=ABCMeta):

	def __init__(self, checkables: t.AbstractSet[Matchable]):
		self._matchables = frozenset(checkables)

	def _and(self, checkable: Matchable):
		return self.__class__(self._matchables | frozenset((checkable,)))

	@abstractmethod
	def match(self, model: searchable) -> bool:
		pass

	def matches(self, models: t.Iterable[searchable]) -> t.Iterable[searchable]:
		return (model for model in models if self.match(model))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__
			and self._matchables == other._matchables
		)

	def __hash__(self):
		return hash((self.__class__, self._matchables))

	def __repr__(self):
		return '{}{}'.format(
			self.__class__.__name__,
			tuple(self._matchables),
		)


class All(Pattern):

	def match(self, model: searchable) -> bool:
		return all(check.match(model) for check in self._matchables)


class Any(Pattern):

	def match(self, model: searchable) -> bool:
		return any(check.match(model) for check in self._matchables)


class Not(Matchable):

	def __init__(self, wrapping: Matchable):
		self._wrapping = wrapping

	def match(self, model: searchable) -> bool:
		return not self._wrapping.match(model)

	def __hash__(self):
		return hash((self.__class__, self._wrapping))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__
			and self._wrapping == other._wrapping
		)

	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			self._wrapping,
		)


class _NotDescriptor(object):

	def __get__(self, instance, owner) -> '_CheckerBuilder':
		instance._negative = True
		return instance


class _CheckerBuilder(object):

	def __init__(self, owner: '_ExtractorBuilder', checker: t.Type[AttributeMatch]):
		self._owner = owner
		self._checker = checker
		self._negative = False

	def __call__(self, value):
		if self._negative:
			self._owner.owner.add(Not(self._checker(self._owner.extractor, value)))
		else:
			self._owner.owner.add(self._checker(self._owner.extractor, value))
		return self._owner.owner

	no = _NotDescriptor()


class _CheckerDescriptor(object):

	def __init__(self, checker: t.Type[AttributeMatch]):
		self.checker = checker

	def __get__(self, instance, owner) -> _CheckerBuilder:
		if instance is None:
			return
		return _CheckerBuilder(instance, self.checker)


class _ExtractorBuilder(object):

	def __init__(self, owner: 'PatternBuilder', extractor: t.Type[Extractor]):
		self.owner = owner
		self.extractor = extractor

	equals = _CheckerDescriptor(Equals) #type: _CheckerBuilder
	greater_than = _CheckerDescriptor(GreaterThan) #type: _CheckerBuilder
	greater_than_or_equals = _CheckerDescriptor(GreaterThanOrEquals) #type: _CheckerBuilder
	less_than = _CheckerDescriptor(LessThan) #type: _CheckerBuilder
	less_than_or_equals = _CheckerDescriptor(LessThanOrEquals) #type: _CheckerBuilder
	contains = _CheckerDescriptor(Contains) #type: _CheckerBuilder
	contained_in = _CheckerDescriptor(ContainedIn) #type: _CheckerBuilder


class PatternBuilder(object, metaclass=ABCMeta):

	def __init__(self):
		self._set = set()

	def add(self, checkable: Matchable) -> 'PatternBuilder':
		self._set.add(checkable)
		return self

	@property
	@abstractmethod
	def name(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def layout(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def cmc(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def rarity(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def flags(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def types(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def mana_cost(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def oracle(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def flavor(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def power(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def toughness(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def loyalty(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def artist(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def expansion(self) -> _ExtractorBuilder:
		pass

	@property
	@abstractmethod
	def block(self) -> _ExtractorBuilder:
		pass

	def all(self) -> All:
		return All(self._set)

	def any(self) -> Any:
		return Any(self._set)


class PrintingPatternBuilder(PatternBuilder):

	def add(self, checkable: Matchable) -> 'PrintingPatternBuilder':
		self._set.add(checkable)
		return self

	@property
	def name(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingNameExtractor)

	@property
	def oracle(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingOracleExtractor)

	@property
	def flavor(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingFlavorExtractor)

	@property
	def power(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingPowerExtractor)

	@property
	def toughness(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingToughnessExtractor)

	@property
	def loyalty(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingLoyaltyExtractor)

	@property
	def artist(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingArtistExtractor)

	@property
	def layout(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingLayoutExtractor)

	@property
	def flags(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingFlagsExtractor)

	@property
	def types(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingTypesExtractor)

	@property
	def rarity(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingRarityExtractor)

	@property
	def cmc(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingCMCExtractor)

	@property
	def mana_cost(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingManaCostExtractor)

	@property
	def expansion(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingExpansionExtractor)

	@property
	def block(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, PrintingBlockExtractor)


class CardboardPatternBuilder(PatternBuilder):

	def add(self, checkable: Matchable) -> 'CardboardPatternBuilder':
		self._set.add(checkable)
		return self

	@property
	def name(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardNameExtractor)

	@property
	def layout(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardLayoutExtractor)

	@property
	def cmc(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardCMCExtractor)

	@property
	def rarity(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardRarityExtractor)

	@property
	def flags(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardFlagsExtractor)

	@property
	def types(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardTypesExtractor)

	@property
	def mana_cost(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardManaCostExtractor)

	@property
	def oracle(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardOracleExtractor)

	@property
	def flavor(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardFlavorExtractor)

	@property
	def power(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardPowerExtractor)

	@property
	def toughness(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardToughnessExtractor)

	@property
	def loyalty(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardLoyaltyExtractor)

	@property
	def artist(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardArtistExtractor)

	@property
	def expansion(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardExpansionExtractor)

	@property
	def block(self) -> _ExtractorBuilder:
		return _ExtractorBuilder(self, CardboardBlockExtractor)


def test():

	from mtgorp.db.load import Loader

	from mtgorp.models.persistent.attributes.flags import Flag
	from mtgorp.models.persistent.attributes.rarities import Rarity
	from mtgorp.models.persistent.attributes import manacosts

	db = Loader.load()

	# pattern = PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).all()
	# print(
	# 	tuple(pattern.matches(db.printings.values()))
	# )
	#
	# another_pattern = PrintingPatternBuilder().power.equals(7).toughness.equals(10).any()
	# print(
	# 	tuple(another_pattern.matches(db.printings.values()))
	# )

	pattern = CardboardPatternBuilder().expansion.equals.no(db.expansions['AKH']).all()

	# third_pattern = All(
	# 	{
	# 		# Any({Equals(PrintingPowerExtractor, 7), Equals(PrintingToughnessExtractor, 10)}),
	# 		# Equals(PrintingCMCExtractor, 7),
	# 		# Not(Contains(PrintingManaCostExtractor, manacosts.ONE_GREEN)),
	# 		# Contains(PrintingFlagsExtractor, Flags((Flag.DRAFT_MATTERS,))),
	# 		Equals(PrintingExpansionExtractor, db.expansions['AKH'])
	# 	}
	# )
	#
	print(
		tuple(
			pattern.matches(db.cardboards.values())
		)
	)

	print(pattern)

if __name__ == '__main__':
	test()