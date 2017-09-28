from models.persistent.artist import Artist
from models.persistent.attributes.rarities import Rarity
from models.persistent.cardboard import Cardboard
from models.persistent.expansion import Expansion
from orp.database import Model, PrimaryKey
from orp.relationships import One, OneDescriptor, DummyOne


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
	primary_key = PrimaryKey(('_expansion', '_collector_number'))
	def __init__(
		self,
		cardboard: Cardboard,
		expansion: Expansion,
		collector_number: int,
		front_artist: Artist = None,
		front_flavor: str = None,
		front_img_id: int = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		back_img_id: int = None,
		rarity: Rarity = None,
	):
		self._expansion = DummyOne(expansion)
		self._collector_number = collector_number
		self._cardboard = One(self, 'printings', cardboard)
		self._expansion = One(self, 'printings', expansion)
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
	def collector_number(self):
		return self._collector_number
	@property
	def front_face(self):
		return self._front_face
	@property
	def back_face(self):
		return self._back_face
	@property
	def faces(self):
		return self.front_face, self.back_face
	def __repr__(self):
		return '{}({}, {})'.format(
			self.__class__.__name__,
			self.expansion.primary_key,
			self._collector_number,
		)

def test():
	a_printing = Printing.__new__(Printing)
	print(dir(a_printing), type(a_printing))
	print(hash(a_printing))

if __name__ == '__main__':
	test()