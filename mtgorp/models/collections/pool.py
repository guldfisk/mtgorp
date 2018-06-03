import typing as t

from mtgorp.models.persistent.printing import Printing
from mtgorp.models.collections.deck import Deck
from mtgorp.utilities.containers import HashableMultiset
from mtgorp.models.collections.serilization.serializeable import Serializeable, SerializationException, model_tree


class Pool(Serializeable):
	
	def __init__(
		self,
		printings: t.Iterable[Printing],
		decks: t.Optional[t.Iterable[Deck]] = None,
	):
		self._printings = (
			printings
			if isinstance(printings, HashableMultiset) else
			HashableMultiset(printings)
		) #type: HashableMultiset[Printing]

		self._decks = (
			()
			if decks is None else
			(
				decks
				if isinstance(decks, tuple) else
				tuple(decks)
			)
		)
	
	@property
	def printings(self) -> HashableMultiset[Printing]:
		return self._printings
	
	@property
	def decks(self) -> t.Tuple[Deck, ...]:
		return self._decks
	
	def __hash__(self) -> int:
		return hash(self._printings)
	
	def __eq__(self, other) -> bool:
		return isinstance(other, Pool) and other.printings == self.printings

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({len(self._printings)}, {len(self._decks)})'

	def to_model_tree(self) -> model_tree:
		return {
			'printings': self._printings,
			'decks': (deck.to_model_tree() for deck in self._decks),
		}

	@classmethod
	def from_model_tree(cls, tree: model_tree) -> 'Pool':
		return Pool(
			tree['printings'],
			(
				Deck.from_model_tree(_tree)
				for _tree in
				tree.get('decks', ())
			)
		)
