import typing as t

from mtgorp.models.persistent.printing import Printing
from mtgorp.models.collections.deck import Deck

from mtgorp.utilities.containers import HashableMultiset

class Pool(object):
	def __init__(
		self,
		printings: t.Iterable[Printing],
		decks: t.Iterable[Deck],
	):
		self._printings = printings if isinstance(printings, HashableMultiset) else HashableMultiset(printings)
		self._decks = decks if isinstance(decks, tuple) else tuple(decks)
	@property
	def printings(self) -> t.FrozenSet[Printing]:
		return self._printings
	@property
	def decks(self) -> t.Tuple[Deck, ...]:
		return self._decks
	def __hash__(self) -> int:
		return hash(self._printings)
	def __eq__(self, other) -> bool:
		return isinstance(other, Pool) and other.printings == self.printings
	