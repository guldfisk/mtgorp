import typing as t

from lazy_property import LazyProperty

from orp.database import Model, PrimaryKey
from orp.relationships import Many

from mtgorp.models.persistent.attributes import typeline, colors, manacosts, powertoughness
from mtgorp.models.interfaces import Cardboard
from mtgorp.models.interfaces import Card as _Card


class Card(Model, _Card):
	primary_key = PrimaryKey('name')

	def __init__(
		self,
		name: str,
		type_line: typeline.TypeLine = None,
		mana_cost: manacosts.ManaCost = None,
		color: t.AbstractSet[colors.Color] = None,
		oracle_text: str = None,
		power_toughness: powertoughness.PowerToughness = None,
		loyalty: powertoughness.PTValue = None,
		color_identity: t.AbstractSet[colors.Color] = None
	):
		self._type_line = type_line
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
	def type_line(self) -> 't.Optional[typeline.TypeLine]':
		return self._type_line

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
	def loyalty(self) -> t.Optional[powertoughness.PTValue]:
		return self._loyalty

	@property
	def color_identity(self) -> 't.Optional[t.AbstractSet[colors.Color]]':
		return self._color_identity

	@LazyProperty
	def cmc(self) -> int:
		return self._mana_cost.cmc if self._mana_cost else 0

	@LazyProperty
	def cardboards(self) -> t.FrozenSet[Cardboard]:
		return frozenset(side.owner for side in self._sides)

	@property
	def cardboard(self) -> t.Optional[Cardboard]:
		try:
			return self.cardboards.__iter__().__next__()
		except StopIteration:
			return None
