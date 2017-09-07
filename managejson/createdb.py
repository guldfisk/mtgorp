import json

from managejson.attributeparse import cardtype, color, manacost, powertoughness

from managejson import download
from managejson.attributeparse.exceptions import AttributeParseException
from models.persistent.attributes import layout
from models.persistent.card import Card
from orp.database import Table


class _CardParser(object):
	layout_switch = {
		'normal': layout.Standard,
		'leveler': layout.Standard,
		'double-faced': layout.Transform,
		'flip': layout.Flip,
		'meld': layout.Meld,
		'split': layout.Split,
		'aftermath': layout.Split,
	}
	@classmethod
	def _parse_colors(cls, cols):
		return {color.Parser.parse(s) for s in cols}
	@classmethod
	def parse(cls, card, tbl: Table):
		try:
			name = card['name']
			layout_type = cls.layout_switch[card['layout']]
		except KeyError:
			raise AttributeParseException()

		if layout_type == layout.Meld:
			layout_type = layout.MeldBack if name == card['names'][-1] else layout.MeldFront

		power, toughness = card.get('power', None), card.get('toughness', None)
		pt = powertoughness.PowerToughness(
			powertoughness.Parser.parse_ptvalue(power),
			powertoughness.Parser.parse_ptvalue(toughness),
		) if power is not None and toughness is not None else None

		try:
			mana_cost = manacost.Parser.parse(card['manaCost'])
		except KeyError:
			mana_cost = None

		c = Card(
			name = name,
			layout_type = layout_type,
			card_type = cardtype.Parser.parse(card.get('type', '')),
			mana_cost = mana_cost,
			color = cls._parse_colors(card.get('colors', ())),
			oracle_text = card.get('text', ''),
			power_toughness = pt,
			loyalty = card.get('loyalty', None),
			color_identity = cls._parse_colors(card.get('colorIdentity', ())),
		)
		if issubclass(layout_type, layout.TwoSided):
			if name == card['names'][0]:
				c.layout._is_front = True
			for other_card in card['names']:
				if other_card != name and other_card in tbl:
					c.layout.other_side = tbl[other_card]
		elif issubclass(layout_type, layout.Split):
			for other_card in card['names']:
				if other_card != name and other_card in tbl:
					c.layout.other_cards.join(tbl[other_card])
		elif issubclass(layout_type, layout.MeldFront):
			other_card = card['names'][-1]
			if other_card in tbl:
				c.layout.back_side = tbl[other_card]
		elif issubclass(layout_type, layout.MeldBack):
			for other_card in card['names']:
				if other_card != name and other_card in tbl:
					c.layout.front_sides.add(tbl[other_card])
		return c

class CardDatabase(object):
	def __init__(
		self,
		cards: Table
	):
		self._cards = cards
	@property
	def cards(self):
		return self._cards

class CardDatabaseCreator(object):
	@classmethod
	def create_card_table(cls, cards):
		table = Table()
		for name in cards:
			try:
				table.insert(
					_CardParser.parse(cards[name], table)
				)
			except AttributeParseException:
				pass
		return table
	@classmethod
	def create_card_database(cls):
		with open(download.ALL_CARDS_PATH, 'r', encoding='UTF-8') as f:
			all_cards = json.load(f)
		return CardDatabase(
			cards = cls.create_card_table(
				all_cards
			)
		)

def test():
	db = CardDatabaseCreator.create_card_database()
	print(
		len(db.cards)
	)
	c = db.cards['Island']
	vs = (
		c.name,
		c.layout,
		c.card_type,
		# c.layout.other_cards,
		c.mana_cost,
		c.oracle_text,
		c.loyalty,
	)

	for item in vs:
		print(item, type(item))

	for item in c.card_type:
		print(item, type(item))

if __name__ == '__main__':
	test()
