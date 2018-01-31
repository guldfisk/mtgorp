import typing as t

from orp.database import Model, PrimaryKey
from orp.relationships import One, OneDescriptor

from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flag
from mtgorp.models.persistent import cardboard as _cardboard
from mtgorp.models.persistent import expansion as _expansion

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
	artist = OneDescriptor('_artist') #type: Artist
	@property
	def owner(self) -> 'Printing':
		return self._owner
	@property
	def flavor(self) -> str:
		return self._flavor

class Printing(Model):
	primary_key = PrimaryKey('id')
	def __init__(
		self,
		id: int,
		expansion: '_expansion.Expansion',
		cardboard: '_cardboard.Cardboard',
		collector_number: int,
		front_artist: Artist = None,
		front_flavor: str = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		rarity: Rarity = None,
		in_booster: bool = True,
		flags: t.Tuple[Flag, ...] = (),
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
		self._in_booster = in_booster
		self._flags = flags
	cardboard = OneDescriptor('_cardboard') #type: _cardboard.Cardboard
	expansion = OneDescriptor('_expansion') #type: _expansion.Expansion
	@property
	def id(self) -> int:
		return self._id
	@property
	def collector_number(self) -> int:
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
	@property
	def rarity(self) -> 'Rarity':
		return self._rarity
	@property
	def in_booster(self) -> bool:
		return self._in_booster
	@property
	def flags(self) -> 't.Tuple[Flag, ...]':
		return self._flags
	def __repr__(self):
		return '{}({}, {}, {})'.format(
			self.__class__.__name__,
			self.cardboard.name,
			self.expansion.code,
			self.id,
		)

def test():
	from mtgorp.models.persistent.card import Card
	a_card = Card('lol')
	another_card = Card('xd')

	a_cardboard = cardboard.Cardboard(
		front_cards = (a_card,),
		back_cards = (another_card,),
	)

	an_expansion = _expansion.Expansion('LOL')
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