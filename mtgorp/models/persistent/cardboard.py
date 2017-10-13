import typing as t
from itertools import chain

from lazy_property import LazyProperty

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.card import Card
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
		front_cards: t.Tuple[Card],
		back_cards: t.Tuple[Card] = None,
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
		return self._front_cards.cards.__iter__().__next__()
	@property
	def back_card(self):
		try:
			return self._back_cards.cards._many[0]
		except IndexError:
			return None

def test():
	a_card = Card('lol')
	another_card = Card('xd')

	a_cardboard = Cardboard(
		front_cards = (a_card,),
		back_cards = (another_card,),
	)

	print(
		a_cardboard,
		a_cardboard.cards,
	)

if __name__ == '__main__':
	test()