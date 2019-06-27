import typing as t
from abc import ABCMeta, abstractmethod, ABC

from mtgorp.models.interfaces import Cardboard, Printing
from mtgorp.tools.search import extraction as e


T = t.TypeVar('T')

searchable = t.Union[Cardboard, Printing]


class Matchable(object):

	@abstractmethod
	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		pass

	def __call__(self, model) -> bool:
		pass


class AttributeMatch(Matchable, metaclass=ABCMeta):

	def __init__(self, extractor: t.Type[e.Extractor], value: t.Union[t.Type[e.Extractor], t.Any]):
		self._extractor = extractor
		self._value = value
		self.__check = (
			self._check_value_is_extractor
			if isinstance(value, type) and issubclass(value, e.Extractor) else
			self._check_value
		)

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__)
			and self._extractor == other._extractor
			and self._value == other._value
		)

	def __hash__(self):
		return hash((self.__class__, self._extractor, self._value))

	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		return any(
			self.__check(extracted, model)
			for extracted in
			self._extractor.extract(model, strategy)
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


class Criteria(Matchable, metaclass=ABCMeta):

	def __init__(self, checkables: t.AbstractSet[Matchable]):
		self._matchables = frozenset(checkables)

	def _and(self, checkable: Matchable):
		return self.__class__(
			self._matchables | frozenset((checkable,))
		)

	@abstractmethod
	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		pass

	def matches(
		self,
		models: t.Iterable[searchable],
		strategy: t.Type[e.ExtractionStrategy],
	) -> t.Iterable[searchable]:
		return (model for model in models if self.match(model, strategy))

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__)
			and self._matchables == other._matchables
		)

	def __hash__(self):
		return hash((self.__class__, self._matchables))

	def __repr__(self):
		return '{}{}'.format(
			self.__class__.__name__,
			tuple(self._matchables),
		)


class All(Criteria):

	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		return all(check.match(model, strategy) for check in self._matchables)


class Any(Criteria):

	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		return any(check.match(model, strategy) for check in self._matchables)


class Not(Matchable):

	def __init__(self, wrapping: Matchable):
		self._wrapping = wrapping

	def match(self, model: searchable, strategy: t.Type[e.ExtractionStrategy]) -> bool:
		return not self._wrapping.match(model, strategy)

	def __hash__(self):
		return hash((self.__class__, self._wrapping))

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__)
			and self._wrapping == other._wrapping
		)

	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			self._wrapping,
		)
	
	
class Pattern(t.Generic[T]):
	
	def __init__(self, matcher: Matchable, strategy: t.Type[e.ExtractionStrategy[T]]):
		self._matcher = matcher
		self._strategy = strategy
		
	def match(self, model: T) -> bool:
		return self._matcher.match(model, self._strategy)

	def matches(self, models: t.Iterable[T]) -> t.Iterable[T]:
		return (
			model
			for model in
			models
			if self._matcher.match(model, self._strategy)
		)

	def __hash__(self):
		return hash((self.__class__, self._matcher, self._strategy))

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._matcher == other._matcher
			and self._strategy == other._strategy
		)

	def __repr__(self):
		return f'{self.__class__.__name__}({self._matcher}, {self._strategy.__name__})'


class _NotDescriptor(object):

	def __get__(self, instance, owner) -> '_CheckerBuilder':
		instance._negative = not instance._negative
		return instance


class _CheckerBuilder(t.Generic[T]):

	def __init__(self, owner: '_ExtractorBuilder[T]', checker: t.Type[AttributeMatch]):
		self._owner = owner
		self._checker = checker
		self._negative = False

	def __call__(self, value) -> 'Builder[T]':
		if self._negative:
			self._owner.owner.add(Not(self._checker(self._owner.extractor, value)))
		else:
			self._owner.owner.add(self._checker(self._owner.extractor, value))

		return self._owner.owner

	no = _NotDescriptor() #type: _CheckerBuilder[T]


class _CheckerDescriptor(object):

	def __init__(self, checker: t.Type[AttributeMatch]):
		self.checker = checker

	def __get__(self, instance, owner) -> _CheckerBuilder:
		if instance is None:
			return
		return _CheckerBuilder(instance, self.checker)


class _ExtractorBuilder(t.Generic[T]):

	def __init__(self, owner: 'Builder[T]', extractor: t.Type[e.Extractor]):
		self.owner = owner
		self.extractor = extractor

	equals = _CheckerDescriptor(Equals) #type: _CheckerBuilder[T]
	greater_than = _CheckerDescriptor(GreaterThan) #type: _CheckerBuilder[T]
	greater_than_or_equals = _CheckerDescriptor(GreaterThanOrEquals) #type: _CheckerBuilder[T]
	less_than = _CheckerDescriptor(LessThan) #type: _CheckerBuilder[T]
	less_than_or_equals = _CheckerDescriptor(LessThanOrEquals) #type: _CheckerBuilder[T]
	contains = _CheckerDescriptor(Contains) #type: _CheckerBuilder[T]
	contained_in = _CheckerDescriptor(ContainedIn) #type: _CheckerBuilder[T]


class Builder(ABC, t.Generic[T]):

	def __init__(self):
		self._set = set()

	def add(self, checkable: Matchable) -> 'Builder[T]':
		self._set.add(checkable)
		return self

	@property
	def name(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.NameExtractor)

	@property
	def oracle(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.OracleExtractor)

	@property
	def flavor(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.FlavorExtractor)

	@property
	def power(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.PowerExtractor)

	@property
	def toughness(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.ToughnessExtractor)

	@property
	def loyalty(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.LoyaltyExtractor)

	@property
	def artist(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.ArtistExtractor)

	@property
	def layout(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.LayoutExtractor)

	@property
	def flags(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.FlagsExtractor)

	@property
	def type_line(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.TypeLineExtractor)

	@property
	def rarity(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.RarityExtractor)

	@property
	def cmc(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.CmcExtractor)

	@property
	def mana_cost(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.ManaCostExtractor)

	@property
	def expansion(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.ExpansionExtractor)

	@property
	def block(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.BlockExtractor)

	@property
	def color(self) -> _ExtractorBuilder[T]:
		return _ExtractorBuilder(self, e.ColorExtractor)

	@abstractmethod
	def all(self) -> T:
		pass

	@abstractmethod
	def any(self) -> T:
		pass


class CriteriaBuilder(Builder[Criteria]):

	def all(self) -> Criteria:
		return All(self._set)

	def any(self) -> Criteria:
		return Any(self._set)


class PrintingPatternBuilder(Builder[Pattern[Printing]]):

	def all(self) -> Pattern[Printing]:
		return Pattern(All(self._set), e.PrintingStrategy)

	def any(self) -> Pattern[Printing]:
		return Pattern(All(self._set), e.PrintingStrategy)


class CardboardPatternBuilder(Builder[Pattern[Cardboard]]):

	def all(self) -> Pattern[Cardboard]:
		return Pattern(All(self._set), e.CardboardStrategy)

	def any(self) -> Pattern[Cardboard]:
		return Pattern(Any(self._set), e.CardboardStrategy)

