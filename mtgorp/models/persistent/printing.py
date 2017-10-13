import typing as t

from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion
from orp.database import Model, PrimaryKey, ForeignOne
from orp.relationships import One, OneDescriptor


class Face(object):
	def __init__(
		self,
		owner,
		artist: Artist = None,
		flavor: str = None,
		img_id: int = None,
	):
		self._owner = owner
		self._artist = One(self, '_faces', artist)
		self._flavor = flavor
		self._img_id = img_id
	artist = OneDescriptor('_artist')
	@property
	def owner(self):
		return self._owner
	@property
	def flavor(self):
		return self._flavor
	@property
	def img_id(self):
		return self._img_id

class Printing(Model):
	primary_key = PrimaryKey(
		(
			ForeignOne('expansion', 'printings'),
			'collector_number',
		)
	)
	def __init__(
		self,
		expansion: Expansion,
		collector_number: str,
		cardboard: Cardboard,
		front_artist: Artist = None,
		front_flavor: str = None,
		front_img_id: int = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		back_img_id: int = None,
		rarity: Rarity = None,
	):
		self._cardboard = One(self, 'printings', cardboard)
		self._front_face = Face(
			self,
			front_artist,
			front_flavor,
			front_img_id,
		)
		self._back_face = Face(
			self,
			back_artist,
			back_flavor,
			back_img_id,
		)
		self._rarity = rarity
	cardboard = OneDescriptor('_cardboard')
	expansion = OneDescriptor('_expansion')
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
		return '{}({}, {})'.format(
			self.__class__.__name__,
			self.expansion.primary_key,
			self._collector_number,
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