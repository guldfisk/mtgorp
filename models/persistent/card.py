import datetime

import typing as t

from orderedset import OrderedSet

from orp.database import Model, PrimaryKey
from orp.relationships import ManyToOne, OneToMany, OneDescriptor, ManyToMany
from models.persistent.attributes import cardtypes, colors, manacosts, powertoughness, layout, raritys, borders

class Card(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name: str,
		layout_type: type = None,
		card_type: cardtypes.CardTypes = None,
		mana_cost: manacosts.ManaCost = None,
		color: t.AbstractSet[colors.Color] = None,
		oracle_text: str = None,
		power_toughness: powertoughness.PowerToughness = None,
		loyalty: int = None,
		color_identity: t.Set[colors.Color] = None
	):
		self._name = name
		self._layout = layout_type(self) if layout_type is not None else layout.Standard(self)
		self._card_type = card_type
		self._mana_cost = mana_cost
		self._color = (
			color if isinstance(color, frozenset) else frozenset(color)
		) if color is not None else frozenset()
		self._oracle_text = oracle_text
		self._power_toughness = power_toughness
		self._loyalty = loyalty
		self._color_identity = color_identity
		self._sides = ManyToMany(self, '_cards')

	@property
	def name(self) -> str:
		return self._name
	@property
	def layout(self):
		return self._layout
	@property
	def card_type(self):
		return self._card_type
	@property
	def mana_cost(self):
		return self._mana_cost
	@property
	def color(self):
		return self._color
	@property
	def oracle_text(self):
		return self._oracle_text
	@property
	def power_toughness(self):
		return self._power_toughness
	@property
	def loyalty(self):
		return self._loyalty
	@property
	def color_identity(self):
		return self._color_identity
	@property
	def cmc(self):
		return self._mana_cost.cmc if self._mana_cost else 0
	@property
	def cardboards(self):
		return {side.owner for side in self._sides}

class Expansion(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name: str,
		code: str,
		release_date: datetime.date = None,
		booster: t.Tuple[str] = None,
		border: borders.Border = None,
		magic_card_info_code: str = None,
		gatherer_code: str = None,
		mkm_name: str = None,
		mkm_id: int = None,
	):
		self._name = name
		self._code = code
		self._release_date = release_date
		self._booster = booster
		self._border = border
		self._magic_card_info_code = magic_card_info_code
		self._gatherer_code = gatherer_code
		self._mkm_name = mkm_name
		self._mkm_id = mkm_id
		self.printings = ManyToOne(self, '_expansion')
	@property
	def name(self):
		return self._name
	@property
	def code(self):
		return self._code
	@property
	def release_date(self):
		return self.release_date
	@property
	def booster(self):
		return self._booster
	@property
	def border(self):
		return self._border
	@property
	def magic_card_info_code(self):
		return self._magic_card_info_code
	@property
	def gatherer_code(self):
		return self._gatherer_code
	@property
	def mkm_name(self):
		return self._mkm_name
	@property
	def mkm_id(self):
		return self._mkm_id

class Artist(Model):
	primary_key = PrimaryKey('name')
	def __init__(self, name: str):
		self.name = name
		self._faces = ManyToOne(self, '_artist')
	@property
	def printings(self):
		return tuple(face.owner for face in self._faces)

class Side(object):
	def __init__(self, owner):
		self._owner = owner
		self._cards = ManyToMany(
			self,
			'_sides',
			container_type = OrderedSet
		)
	@property
	def owner(self):
		return self._owner
	@property
	def cards(self):
		return self._cards

class Cardboard(Model):
	primary_key = PrimaryKey('name')
	_SPLIT_SEPARATOR = ' // '
	def __init__(
		self,
		front_cards: t.Iterable[Card],
		back_cards: t.Iterable[Card] = None,
	):
		self._front_cards = Side(self)
		for c in front_cards:
			self._front_cards.cards.add(c)
		self._back_cards = Side(self)
		if back_cards is not None:
			for c in back_cards:
				self._back_cards.cards.add(c)
		self._name = self._calc_name()
		self.printings = ManyToOne(self, '_expansion')
	def _calc_name(self):
		return self.__class__._SPLIT_SEPARATOR.join(
			c.name
			for c in
			self._front_cards.cards
		)
	@property
	def name(self):
		return self._name
	@property
	def main(self):
		try:
			return self._front_cards.cards._many[0]
		except IndexError:
			return None
	@property
	def front_cards(self):
		return self._front_cards.cards
	@property
	def back_cards(self):
		return self._back_cards.cards

class Face(object):
	def __init__(
		self,
		owner,
		artist: Artist = None,
		flavor: str = None,
		img_id: int = None,
	):
		self._owner = owner
		self._artist = OneToMany(self, '_faces', artist)
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
	primary_key = PrimaryKey('id')
	def __init__(
		self,
		cardboard: Cardboard,
		expansion: Expansion,
		front_artist: Artist = None,
		front_flavor: str = None,
		front_img_id: int = None,
		back_artist: Artist = None,
		back_flavor: str = None,
		back_img_id: int = None,
		rarity: raritys.Rarity = None,
	):
		self.id = self._incrementer()
		self._cardboard = OneToMany(self, 'printings', cardboard)
		self._expansion = OneToMany(self, 'cards', expansion)
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
	def front_face(self):
		return self._front_face
	@property
	def back_face(self):
		return self._back_face
	def __repr__(self):
		return '{}({}, {}, {})'.format(
			self.__class__.__name__,
			self.cardboard.primary_key,
			self.expansion.primary_key,
			self.id,
		)

def test():
	fire = Card('Fire')
	ice = Card('Ice')
	acb = Cardboard(
		(fire, ice)
	)
	ae = Expansion('an expansion', 'aex')
	apr = Printing(acb, ae)
	print(apr)

if __name__ == '__main__':
	test()