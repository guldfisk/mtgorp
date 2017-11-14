import typing as t

from lazy_property import LazyProperty

from mtgorp.models.persistent.attributes import cardtypes, colors, manacosts, powertoughness
from mtgorp.models.persistent import cardboard as _cardboard
from orp.database import Model, PrimaryKey
from orp.relationships import Many

class Card(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name: str,
		card_type: cardtypes.CardTypes = None,
		mana_cost: manacosts.ManaCost = None,
		color: t.AbstractSet[colors.Color] = None,
		oracle_text: str = None,
		power_toughness: powertoughness.PowerToughness = None,
		loyalty: int = None,
		color_identity: t.AbstractSet[colors.Color] = None
	):
		self._card_type = card_type
		self._mana_cost = mana_cost
		self._color = (
			color if isinstance(color, frozenset) else frozenset(color)
		) if color is not None else frozenset()
		self._oracle_text = oracle_text
		self._power_toughness = power_toughness
		self._loyalty = loyalty
		self._color_identity = color_identity
		self._sides = Many(self, '_cards')
	@property
	def name(self) -> str:
		return self._name
	@property
	def card_type(self) -> 't.Optional[cardtypes.CardType]':
		return self._card_type
	@property
	def mana_cost(self) -> 't.Optional[manacosts.ManaCost]':
		return self._mana_cost
	@property
	def color(self) -> 't.Optional[t.AbstractSet[colors.Color]]':
		return self._color
	@property
	def oracle_text(self) -> t.Optional[str]:
		return self._oracle_text
	@property
	def power_toughness(self) -> 't.Optional[powertoughness.PowerToughness]':
		return self._power_toughness
	@property
	def loyalty(self) -> t.Optional[int]:
		return self._loyalty
	@property
	def color_identity(self) -> 't.Optional[t.AbstractSet[colors.Color]]':
		return self._color_identity
	@LazyProperty
	def cmc(self) -> int:
		return self._mana_cost.cmc if self._mana_cost else 0
	@LazyProperty
	def cardboards(self) -> 't.FrozenSet[_cardboard.Cardboard]':
		return frozenset(side.owner for side in self._sides)
	@property
	def cardboard(self) -> 't.Optional[_cardboard.Cardboard]':
		try:
			return self.cardboards.__iter__().__next__()
		except StopIteration:
			return None

def test():
	pass
	# fire = Card('Fire')
	# ice = Card('Ice')
	# insectile_abberation = Card('Insectile Abberation')
	# a_cardboard = Cardboard(
	# 	(fire, ice),
	# 	(insectile_abberation,)
	# )
	# another_cardboard = Cardboard(
	# 	(ice, ice)
	# )
	# an_expansion = Expansion('an expansion', 'aex')
	# a_printing = Printing(a_cardboard, an_expansion)
	# another_printing = Printing(another_cardboard, an_expansion)
	# print(
	# 	a_printing,
	# 	another_printing,
	# )
	# vs = (
	# 	an_expansion.printings,
	# 	a_printing.cardboard,
	# 	a_cardboard,
	# 	a_cardboard.printings,
	# 	ice,
	# 	ice.cardboards,
	# 	fire.cardboards,
	# )
	#
	# for v in vs:
	# 	print(v)

if __name__ == '__main__':
	test()