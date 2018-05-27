import typing as t

from orp.database import Table

from mtgorp.models.interfaces import Card, Cardboard, Printing, Artist, Block, Expansion


class CardDatabase(object):

	def __init__(
		self,
		cards: Table,
		cardboards: Table,
		printings: Table,
		artists: Table,
		blocks: Table,
		expansions: Table,
	):
		self._cards = cards
		self._cardboards = cardboards
		self._printings = printings
		self._artists = artists
		self._blocks = blocks
		self._expansions = expansions

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
