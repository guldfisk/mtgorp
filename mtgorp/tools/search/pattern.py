import typing as t
from abc import ABCMeta, abstractmethod

from mtgorp.models.interfaces import Cardboard, Printing


searchable = t.Union[Cardboard, Printing]


class Extractor(object, metaclass=ABCMeta):

	@staticmethod
	@abstractmethod
	def extract(model) -> t.Iterable[t.Any]:
		pass


class PrintingLayoutExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return printing.cardboard.layout,


class CardboardLayoutExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return cardboard.layout,


class PrintingCMCExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (card.cmc for card in printing.cardboard.cards)


class CardboardCMCExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (card.cmc for card in cardboard.cards)


class PrintingRarityExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return printing.rarity,


class CardboardRarityExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (printing.rarity for printing in cardboard.printings)


class PrintingFlagsExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return printing.flags,


class CardboardFlagExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (printing.flags for printing in cardboard.printings)


class PrintingTypesExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (card.type_line for card in printing.cardboard.cards)


class CardboardTypesExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (card.type_line for card in cardboard.cards)


class PrintingManaCostExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (card.mana_cost for card in printing.cardboard.cards)


class CardboardManaCostExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (card.mana_cost for card in cardboard.cards)


class PrintingOracleExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (card.oracle_text for card in printing.cardboard.cards)


class CardboardOracleExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (card.oracle_text for card in cardboard.cards)


class PrintingFlavorExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (face.flavor for face in printing.faces)


class CardboardFlavorExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (face.flavor for printing in cardboard.printings for face in printing.faces)


class PrintingPowerExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (
			card.power_toughness.power
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)


class CardboardPowerExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (
			card.power_toughness.power
			if card.power_toughness is not None else
			None
			for card in
			cardboard.cards
		)


class PrintingToughnessExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (
			card.power_toughness.toughness
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)


class CardboardToughnessExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (
			card.power_toughness.toughness
			if card.power_toughness is not None else
			None
			for card in
			cardboard.cards
		)


class PrintingLoyaltyExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (card.loyalty for card in printing.cardboard.cards)


class CardboardLoyaltyExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (card.loyalty for card in cardboard.cards)


class PrintingArtistExtractor(Extractor):

	@staticmethod
	def extract(printing: Printing) -> t.Iterable[t.Any]:
		return (face.artist for face in printing.faces)


class CardboardArtistExtractor(Extractor):

	@staticmethod
	def extract(cardboard: Cardboard) -> t.Iterable[t.Any]:
		return (face.artist for printing in cardboard.printings for face in printing.faces)


class Matchable(object):
	@abstractmethod
	def match(self, model: searchable) -> bool:
		pass

	def __call__(self, model) -> bool:
		pass


class AttributeMatch(Matchable, metaclass=ABCMeta):

	def __init__(self, extractor: t.Type[Extractor], value):
		self._extractor = extractor
		self._value = value

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
			extracted is not None and self.check(extracted)
			for extracted in
			self._extractor.extract(model)
		)

	@abstractmethod
	def check(self, remote) -> bool:
		pass

	def __repr__(self) -> str:
		return '{}({}, {})'.format(
			self.__class__.__name__,
			self._extractor.__name__,
			self._value,
		)


class Equals(AttributeMatch):

	def check(self, remote) -> bool:
		return self._value == remote


class GreaterThan(AttributeMatch):

	def check(self, remote) -> bool:
		return remote > self._value


class GreaterThanOrEquals(AttributeMatch):

	def check(self, remote) -> bool:
		return remote >= self._value


class LessThan(AttributeMatch):

	def check(self, remote) -> bool:
		return remote < self._value


class LessThanOrEquals(AttributeMatch):

	def check(self, remote) -> bool:
		return remote <= self._value


class Contains(AttributeMatch):

	def check(self, remote) -> bool:
		return self._value in remote


class ContainedIn(AttributeMatch):

	def check(self, remote) -> bool:
		return remote in self._value


class NotContains(AttributeMatch):

	def check(self, remote) -> bool:
		return not self._value in remote


class Pattern(Matchable, metaclass=ABCMeta):

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


class _CheckerBuilder(object):

	def __init__(self, owner: '_ExtractorBuilder', checker: t.Type[AttributeMatch]):
		self.owner = owner
		self.checker = checker

	def __call__(self, value):
		self.owner.owner._add(self.checker(self.owner.extractor, value))
		return self.owner.owner


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

	def _add(self, checkable: Matchable):
		self._set.add(checkable)

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

	def all(self) -> All:
		return All(self._set)

	def any(self) -> Any:
		return Any(self._set)


class PrintingPatternBuilder(PatternBuilder):

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


class CardboardPatternBuilder(PatternBuilder):

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
		return _ExtractorBuilder(self, CardboardFlagExtractor)

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

	third_pattern = All(
		{
			Any({Equals(PrintingPowerExtractor, 7), Equals(PrintingToughnessExtractor, 10)}),
			Equals(PrintingCMCExtractor, 7),
			Not(Contains(PrintingManaCostExtractor, manacosts.ONE_GREEN)),
		}
	)

	print(
		tuple(
			third_pattern.matches(db.printings.values())
		)
	)

	print(
		third_pattern,
	)

if __name__ == '__main__':
	test()