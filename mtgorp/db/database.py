import typing as t

from orp.database import Table, Database

from mtgorp.models.persistent.card import Card
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.printing import Printing
from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.block import Block
from mtgorp.models.persistent.expansion import Expansion


class CardDatabase(Database):

	def __init__(
		self,
		cards: Table,
		cardboards: Table,
		printings: Table,
		artists: Table,
		blocks: Table,
		expansions: Table,
	):
		super().__init__(
			{
				Card: cards,
				Cardboard: cardboards,
				Printing: printings,
				Artist: artists,
				Block: blocks,
				Expansion: expansions,
			}
		)
		self._cards = self._tables[Card]
		self._cardboards = self._tables[Cardboard]
		self._printings = self._tables[Printing]
		self._artists = self._tables[Artist]
		self._blocks = self._tables[Block]
		self._expansions = self._tables[Expansion]

	@property
	def cards(self) -> t.Dict[str, Card]:
		return self._cards

	@property
	def cardboards(self) -> t.Dict[str, Cardboard]:
		return self._cardboards

	@property
	def printings(self) -> t.Dict[int, Printing]:
		return self._printings

	@property
	def artists(self) -> t.Dict[str, Artist]:
		return self._artists

	@property
	def blocks(self) -> t.Dict[str, Block]:
		return self._blocks

	@property
	def expansions(self) -> t.Dict[str, Expansion]:
		return self._expansions
