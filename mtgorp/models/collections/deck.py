import typing as t

from mtgorp.models.persistent.printing import Printing

from mtgorp.utilities.containers import HashableMultiset

class Deck(object):
	def __init__(self, maindeck: t.Iterable[Printing], sideboard: t.Iterable[Printing] = None):
		self._maindeck = maindeck if isinstance(maindeck, HashableMultiset) else HashableMultiset(maindeck)
		self._sideboard = (
			(
				sideboard
				if isinstance(sideboard, HashableMultiset) else
				HashableMultiset(sideboard)
			)
			if sideboard is not None else
			HashableMultiset()
		)
	@property
	def maindeck(self) -> t.FrozenSet[Printing]:
		return self._maindeck
	@property
	def sideboard(self) -> t.FrozenSet[Printing]:
		return self._sideboard
	@property
	def seventy_five(self) -> t.FrozenSet[Printing]:
		return self._maindeck + self._sideboard
	def __iter__(self) -> t.Iterable[Printing]:
		return self.seventy_five.__iter__()
	def __eq__(self, other) -> bool:
		return isinstance(other, Deck) and other.seventy_five == self.seventy_five
	def __hash__(self) -> int:
		return hash(self.seventy_five)
