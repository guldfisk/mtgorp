import typing as t
from itertools import chain

from lazy_property import LazyProperty

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.card import Card
from mtgorp.models.persistent import expansion as _expansion
from mtgorp.models.persistent import printing as _printing
from orp.database import Model, PrimaryKey, Key
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
	primary_key = PrimaryKey(
		Key(
			'name',
			calc_value = lambda k, o, m: o.__class__.calc_name(
				c.name
				for c in
				(
					chain(m['front_cards'], m['back_cards'])
					if m['back_cards'] is not None else
					m['front_cards']
				)
			),
			input_values = ('front_cards', 'back_cards'),
		)
	)
	_SPLIT_SEPARATOR = ' // '

	def __init__(
		self,
		front_cards: t.Tuple[Card, ...],
		back_cards: t.Tuple[Card, ...] = None,
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
		self.printings = Many(self, '_cardboard') #type: t.Set[_printing.Printing]

	@classmethod
	def calc_name(cls, names) -> str:
		return cls._SPLIT_SEPARATOR.join(names)

	@property
	def name(self) -> str:
		return self._name

	@property
	def front_cards(self) -> 't.Tuple[Card]':
		return self._front_cards.cards

	@property
	def back_cards(self) -> 't.Tuple[Card]':
		return self._back_cards.cards

	@LazyProperty
	def cards(self) -> 't.Tuple[Card, ...]':
		return tuple(self.front_cards)+tuple(self.back_cards)

	@property
	def layout(self) -> Layout:
		return self._layout

	@property
	def front_card(self) -> Card:
		return self._front_cards.cards.__iter__().__next__()

	@property
	def back_card(self) -> 't.Optional[Card]':
		try:
			return self._back_cards.cards._many[0]
		except IndexError:
			return None

	@property
	def printing(self) -> '_printing.Printing':
		return self.printings.__iter__().__next__()

	def from_expansion(self, expansion: 't.Union[_expansion.Expansion, str]') -> '_printing.Printing':
		if isinstance(expansion, _expansion.Expansion):
			for printing in self.printings:
				if printing.expansion==expansion:
					return printing
		else:
			for printing in self.printings:
				if printing.expansion.code==expansion:
					return printing
		raise KeyError(
			'{} not printed in {}'.format(
				self,
				expansion,
			)
		)
