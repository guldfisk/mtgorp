import typing as t

from orp.database import Model, PrimaryKey
from orp.relationships import One, OneDescriptor

from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flag, Flags
from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.models.interfaces import Artist, Cardboard, Expansion
from mtgorp.models.interfaces import Face as _Face
from mtgorp.models.interfaces import Printing as _Printing


class Face(_Face):

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


class Printing(Model, _Printing):
	primary_key = PrimaryKey('id')

	def __init__(
		self,
		id: int,
		expansion: Expansion,
		cardboard: Cardboard,
		collector_number: int,
		front_artist: Artist = None,
		front_flavor: str = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		rarity: Rarity = None,
		in_booster: bool = True,
		flags: t.Optional[Flags] = None,
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
		self._flags = Flags() if flags is None else flags

	cardboard = OneDescriptor('_cardboard') #type: Cardboard
	expansion = OneDescriptor('_expansion') #type: Expansion

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
	def flags(self) -> Flags:
		return self._flags

	@property
	def border(self) -> t.Optional[Border]:
		return self.expansion.border

	def __repr__(self):
		return '{}({}, {}, {})'.format(
			self.__class__.__name__,
			self.cardboard.name,
			self.expansion.code,
			self.id,
		)