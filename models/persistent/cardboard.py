import typing as t

from lazy_property import LazyProperty

from models.persistent.attributes.layout import Layout
from models.persistent.card import Card
from orp.database import Model, PrimaryKey
from orp.relationships import Many


class OrderedMultiSet(list):
	def add(self, element):
		self.append(element)

class Side(object):
	def __init__(self, owner):
		self._owner = owner
		self._cards = Many(
			self,
			'_sides',
			container_type = OrderedMultiSet,
		)
	@property
	def owner(self):
		return self._owner
	@property
	def cards(self):
		return self._cards

class Cardboard(Model):
	primary_key = PrimaryKey('_name')
	_SPLIT_SEPARATOR = ' // '
	def __init__(
		self,
		front_cards: t.Iterable[Card],
		back_cards: t.Iterable[Card] = None,
		layout: Layout = Layout.STANDARD,
	):
		self._front_cards = Side(self)
		for c in front_cards:
			self._front_cards.cards.add(c)
		self._back_cards = Side(self)
		if back_cards is not None:
			for c in back_cards:
				self._back_cards.cards.add(c)
		self._layout = layout
		self.printings = Many(self, '_cardboard')
		self._name = self.__class__.calc_name(
			c.name
			for c in
			self.cards
		)
	@classmethod
	def calc_name(cls, names):
		return cls._SPLIT_SEPARATOR.join(names)
	@property
	def name(self):
		return self._name
	@property
	def front_cards(self):
		return self._front_cards.cards
	@property
	def back_cards(self):
		return self._back_cards.cards
	@LazyProperty
	def cards(self):
		return tuple(self.front_cards)+tuple(self.back_cards)
	@property
	def layout(self):
		return self._layout
	@property
	def front_card(self):
		try:
			return self._front_cards.cards._many[0]
		except IndexError:
			return None
	@property
	def back_card(self):
		try:
			return self._back_cards.cards._many[0]
		except IndexError:
			return None
