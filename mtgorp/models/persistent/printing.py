import typing as t

from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion
from orp.database import Model, PrimaryKey
from orp.relationships import One, OneDescriptor


class Face(object):
	def __init__(
		self,
		owner,
		artist: Artist = None,
		flavor: str = None,
	):
		self._owner = owner
		self._artist = One(self, '_faces', artist)
		self._flavor = flavor
	artist = OneDescriptor('_artist')
	@property
	def owner(self):
		return self._owner
	@property
	def flavor(self):
		return self._flavor

class Printing(Model):
	primary_key = PrimaryKey('id')
	def __init__(
		self,
		id: int,
		expansion: Expansion,
		cardboard: Cardboard,
		collector_number: str = None,
		front_artist: Artist = None,
		front_flavor: str = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		rarity: Rarity = None,
	):
		self._expansion = One(self, 'printings', expansion)
		self._cardboard = One(self, 'printings', cardboard)
		self._collector_number = collector_number
		self._front_face = Face(
			self,
			front_artist,
			front_flavor,
		)
		self._back_face = Face(
			self,
			back_artist,
			back_flavor,
		)
		self._rarity = rarity
	cardboard = OneDescriptor('_cardboard')
	expansion = OneDescriptor('_expansion')
	@property
	def id(self) -> int:
		return self._id
	@property
	def collector_number(self) -> str:
		return self._collector_number
	@property
	def front_face(self) -> Face:
		return self._front_face
	@property
	def back_face(self) -> Face:
		return self._back_face
	@property
	def faces(self) -> t.Tuple[Face, Face]:
		return self.front_face, self.back_face
	def __repr__(self):
		return '{}({}, {}, {})'.format(
			self.__class__.__name__,
			self.expansion.primary_key,
			self._collector_number,
			self.id,
		)

def test():
	from mtgorp.models.persistent.card import Card
	a_card = Card('lol')
	another_card = Card('xd')

	a_cardboard = Cardboard(
		front_cards = (a_card,),
		back_cards = (another_card,),
	)

	an_expansion = Expansion('LOL')
	a_printing = Printing(
		expansion = an_expansion,
		collector_number = '1',
		cardboard = a_cardboard
	)

	print(
		a_printing
	)

if __name__ == '__main__':
	test()