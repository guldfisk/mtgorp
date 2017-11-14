import typing as t
from abc import ABCMeta, abstractmethod, abstractstaticmethod

from mtgorp.models.persistent import printing as _printing
from orp.database import Model

class Extractor(object):
	@staticmethod
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

class Checkable(object):
	def __call__(self, model) -> bool:
		pass

class Checker(Checkable, metaclass=ABCMeta):
	def __init__(self, extractor: Extractor, value):
		self._extractor = extractor
		self._value = value
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self._extractor == other._extractor
	def __hash__(self):
		return hash((self.__class__, self._extractor))
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
	def build(self) -> All:
		return All(self._set)

class PrintingPatternBuilder(PatternBuilder):
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

	import time
	from mtgorp.db.load import Loader
	from mtgorp.models.persistent.attributes import manacosts as mc
	from mtgorp.tools.search.oldsearch import PrintingPatternBuilder as _PrintingPatternBuilder

	class Timer(object):
		def __init__(self):
			self.current_time = 0
		def middle_time(self):
			v = time.time() - self.current_time
			self.current_time = time.time()
			return v

	timer = Timer()
	timer.middle_time()

	# create.update_database()

	print('update done', timer.middle_time())

	db = Loader.load()

	print('load done', timer.middle_time())

	a_mana_cost = mc.ManaCost((mc.ONE_GENERIC,)+(mc.ONE_BLUE,))
	another_mana_cost = mc.ManaCost((mc.ONE_GENERIC,)*2+(mc.ONE_BLUE,))

	pattern = PrintingPatternBuilder().mana_cost.contains(a_mana_cost).mana_cost.contained_in(another_mana_cost).build()
	old_pattern = _PrintingPatternBuilder().mana_cost.contains(a_mana_cost).mana_cost.contained_in(another_mana_cost).build()
	# pattern = PrintingPatternBuilder().cmc.equals(a_mana_cost)

	print('pattern build', timer.middle_time())

	printings = tuple(printing for printing in db.printings.values() if pattern.match(printing))

	print('search complete', timer.middle_time())

	print(
		len(printings),
	)

	printings = tuple(printing for printing in db.printings.values() if pattern.match(printing))

	print('second search complete', timer.middle_time())

	print(
		len(printings),
	)

	printings = tuple(printing for printing in db.printings.values() if old_pattern.match(printing))

	print('second search complete', timer.middle_time())

	print(
		len(printings),
	)


if __name__ == '__main__':
	test()