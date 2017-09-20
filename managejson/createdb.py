import json

from managejson import download
from managejson.attributeparse import cardtype, color, manacost, powertoughness
from managejson.attributeparse.exceptions import AttributeParseException
from models.persistent.attributes.layout import Layout
from models.persistent.card import Card
from models.persistent.cardboard import Cardboard
from orp.database import Table


class _CardParser(object):
	@classmethod
	def _parse_colors(cls, cols):
		return {color.Parser.parse(s) for s in cols}
	@classmethod
	def parse(cls, raw_card):
		try:
			name = raw_card['name']
		except KeyError:
			raise AttributeParseException()

		power, toughness = raw_card.get('power', None), raw_card.get('toughness', None)
		pt = powertoughness.PowerToughness(
			powertoughness.Parser.parse_ptvalue(power),
			powertoughness.Parser.parse_ptvalue(toughness),
		) if power is not None and toughness is not None else None

		try:
			mana_cost = manacost.Parser.parse(raw_card['manaCost'])
		except KeyError:
			mana_cost = None

		card = Card(
			name = name,
			card_type = cardtype.Parser.parse(raw_card.get('type', '')),
			mana_cost = mana_cost,
			color = cls._parse_colors(raw_card.get('colors', ())),
			oracle_text = raw_card.get('text', ''),
			power_toughness = pt,
			loyalty = raw_card.get('loyalty', None),
			color_identity = cls._parse_colors(raw_card.get('colorIdentity', ())),
		)
		return card

LAYOUT_SWITCH = {
	'normal': Layout.STANDARD,
	'leveler': Layout.STANDARD,
	'double-faced': Layout.TRANSFORM,
	'flip': Layout.FLIP,
	'meld': Layout.MELD,
	'split': Layout.SPLIT,
	'aftermath': Layout.SPLIT,
}

class _CardboardParser(object):
	@classmethod
	def parse(cls, raw_card, cards: Table):
		try:
			name = raw_card['name']
			layout = LAYOUT_SWITCH[raw_card['layout']]

			if layout == Layout.STANDARD:
				return Cardboard(
					(cards[name],)
				)
			elif layout == Layout.SPLIT or layout == Layout.FLIP:
				if name == raw_card['names'][0]:
					return Cardboard(
						(cards[n] for n in raw_card['names']),
						None,
						layout,
					)
			elif layout == Layout.TRANSFORM:
				if name == raw_card['names'][0]:
					return Cardboard(
						(cards[name],),
						(cards[raw_card['names'][1]],),
						layout,
					)
			elif layout == Layout.MELD:
				if name in raw_card['names'][0:1]:
					return Cardboard(
						(cards[name],),
						(cards[raw_card['names'][-1]],),
						layout,
					)
			raise AttributeParseException()
		except KeyError:
			raise AttributeParseException()

class _ExpansionParser(object):
	@classmethod
	def _parse_printing(self, raw_printing, artists: Table):
		try:
			name = raw_printing['name']
			layout = LAYOUT_SWITCH[raw_printing['layout']]

			if layout == Layout.STANDARD:
				pass
		except KeyError:
			raise AttributeParseException()

	@classmethod
	def parse(cls, raw_expansion, cardboards: Table, printings: Table, artists: Table):
		pass

class CardDatabase(object):
	def __init__(
		self,
		cards: Table,
		cardboards: Table = None,
	):
		self._cards = cards
		self._cardboards = cardboards
	@property
	def cards(self):
		return self._cards
	@property
	def cardboards(self):
		return self._cardboards

class CardDatabaseCreator(object):
	@classmethod
	def create_card_table(cls, raw_cards):
		cards = Table()
		for name in raw_cards:
			try:
				cards.insert(
					_CardParser.parse(raw_cards[name])
				)
			except AttributeParseException:
				pass
		return cards
	@classmethod
	def create_cardboard_table(cls, raw_cards, cards):
		cardboards = Table()
		for name in raw_cards:
			try:
				cardboards.insert(
					_CardboardParser.parse(raw_cards[name], cards)
				)
			except AttributeParseException:
				pass
		return cardboards
	@classmethod
	def create_card_database(cls):
		with open(download.ALL_CARDS_PATH, 'r', encoding='UTF-8') as f:
			raw_cards = json.load(f)
		cards = cls.create_card_table(raw_cards)
		cardboards = cls.create_cardboard_table(raw_cards, cards)
		# cardboards = None
		return CardDatabase(
			cards = cards,
			cardboards = cardboards,
		)

def test():
	db = CardDatabaseCreator.create_card_database()
	print(
		len(db.cards)
	)
	c = db.cards["Delver of Secrets"]

	inspections = (
		"name",
		"card_type",
		"mana_cost",
		"oracle_text",
		"loyalty",
	)

	def ppcard(c):
		for item in inspections:
			print(
				item,
				getattr(c, item),
			)

	# cb = db.cardboards["Bruna, the Fading Light // Brisela, Voice of Nightmares"]
	cb = tuple(c.cardboards)[0]

	print(cb, cb.layout)
	for card in cb.front_cards:
		ppcard(card)

if __name__ == '__main__':
	test()
