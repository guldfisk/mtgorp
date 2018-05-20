import typing as t

from mtgorp.models.interfaces import Printing, Expansion
from mtgorp.models.interfaces import Booster as _Booster

from mtgorp.utilities.containers import HashableMultiset


class Booster(_Booster):

	def __init__(self, printings: t.Iterable[Printing], expansion: Expansion = None):
		self._printings = printings if isinstance(printings, HashableMultiset) else HashableMultiset(printings)
		self._expansion = expansion

	@property
	def printings(self) -> HashableMultiset[Printing]:
		return self._printings

	@property
	def sorted_printings(self) -> t.List[Printing]:
		return sorted(self._printings, key=lambda p: p.rarity.value, reverse=True)

	@property
	def expansion(self):
		return self._expansion

	def __str__(self) -> str:
		return '{}({})'.format(
			self.__class__.__name__,
			tuple(a_printing.cardboard.name for a_printing in self.sorted_printings),
		)

	def __contains__(self, printing: Printing) -> bool:
		return printing in self._printings

	def __iter__(self) -> t.Iterable[Printing]:
		return self._printings.__iter__()

