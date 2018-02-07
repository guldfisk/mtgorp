import typing as t
from abc import ABCMeta, abstractmethod, abstractstaticmethod

from mtgorp.models.persistent import printing as _printing
from orp.database import Model

class Extractor(object, metaclass=ABCMeta):
	@staticmethod
	@abstractmethod
	def extract(model) -> t.Iterable[t.Any]:
		pass

class PrintingLayoutExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return printing.cardboard.layout,

class PrintingCMCExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (card.cmc for card in printing.cardboard.cards)

class PrintingRarityExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return printing.rarity,

class PrintingFlagsExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return printing.flags,

class PrintingTypesExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (card.card_type for card in printing.cardboard.cards)

class PrintingManaCostExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (card.mana_cost for card in printing.cardboard.cards)

class PrintingOracleExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (card.oracle_text for card in printing.cardboard.cards)

class PrintingFlavorExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (face.flavor for face in printing.faces)

class PrintingPowerExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (
			card.power_toughness.power
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)

class PrintingToughnessExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (
			card.power_toughness.toughness
			if card.power_toughness is not None else
			None
			for card in
			printing.cardboard.cards
		)

class PrintingLoyaltyExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (card.loyalty for card in printing.cardboard.cards)

class PrintingArtistExtractor(Extractor):
	@staticmethod
	def extract(printing: '_printing.Printing'):
		return (face.artist for face in printing.faces)

class Checkable(object):
	def __call__(self, model) -> bool:
		pass

class Checker(Checkable, metaclass=ABCMeta):
	def __init__(self, extractor: Extractor, value):
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
	def __call__(self, model) -> bool:
		return any(
			extracted is not None and self.check(self._value, extracted)
			for extracted in
			self._extractor.extract(model)
		)
	@abstractstaticmethod
	def check(stored, remote) -> bool:
		pass

class Equals(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return stored == remote

class GreaterThan(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return remote > 5

class GreaterThanOrEquals(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return remote >= 5

class LessThan(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return remote < 5

class LessThanOrEquals(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return remote <= 5

class Contains(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return stored in remote

class ContainedIn(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return remote in stored
	
class NotContains(Checker):
	@staticmethod
	def check(stored, remote) -> bool:
		return not stored in remote

class Pattern(object, metaclass=ABCMeta):
	def __init__(self, checkables: t.AbstractSet[Checkable]):
		self._checkables = frozenset(checkables)
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self._checkables == other._checkables
	def __hash__(self):
		return hash((self.__class__, self._checkables))
	def _and(self, checkable: Checkable):
		return Pattern(self._checkables | frozenset((checkable,)))
	@abstractmethod
	def match(self, model: Model) -> bool:
		pass
	def matches(self, models: t.Iterable[Model]) -> t.Iterable[Model]:
		return (model for model in models if self.match(model))

class All(Pattern):
	def match(self, model: Model) -> bool:
		return all(check(model) for check in self._checkables)

class _CheckerBuilder(object):
	def __init__(self, owner: '_ExtractorBuilder', checker: type):
		self.owner = owner
		self.checker = checker
	def __call__(self, value):
		self.owner.owner._add(self.checker(self.owner.extractor, value))
		return self.owner.owner

class _CheckerDescriptor(object):
	def __init__(self, checker: type):
		self.checker = checker
	def __get__(self, instance, owner) -> _CheckerBuilder:
		if instance is None:
			return
		return _CheckerBuilder(instance, self.checker)

class _ExtractorBuilder(object):
	def __init__(self, owner: 'PatternBuilder', extractor: type):
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
	def _add(self, checkable: Checkable):
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
	def build(self) -> All:
		return All(self._set)

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

def test():

	from mtgorp.db.load import Loader

	from mtgorp.models.persistent.attributes.flags import Flag
	from mtgorp.models.persistent.attributes.rarities import Rarity

	db = Loader.load()

	print(db.printings['Agent of Acquisitions'])


	pattern = PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).build()
	print(
		tuple(pattern.matches(db.printings.values()))
	)


	another_pattern = PrintingPatternBuilder().power.equals(7).toughness.equals(10).build()
	print(
		tuple(another_pattern.matches(db.printings.values()))
	)


if __name__ == '__main__':
	test()