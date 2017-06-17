import copy
import json
import os
import random
import re
import xml.etree.ElementTree as ET

from resourceload import locate
from resourceload.cardload import CardLoader

#Returns names from list which are not magic names
def checkList(cards, names=None):
	if names is None:
		names = CardLoader.get_cards_name_list()
	return set(card for card in cards if not card in names)

class Card(dict):
	def __hash__(self):
		return hash(id(self))
	def __eq__(self, other):
		return id(self)==id(other)
	class CardView(object):
		def invalid(card):
			return 'INVALID STYLE'
		def name(card):
			name_add = ''
			if card.get('layout', False) == 'split' and 'names' in card and len(card['names'])>1:
				name_add = ' // '+[obj for obj in card['names'] if obj!=card['name']][0]
			elif card.get('layout', False) == 'flip' and 'names' in card and len(card['names'])>1:
				name_add = '  '+[obj for obj in card['names'] if obj!=card['name']][0]
			elif card.get('layout', False) == 'double-faced' and 'names' in card and len(card['names'])>1:
				name_add = ' >> '+[obj for obj in card['names'] if obj!=card['name']][0]
			return str(card.get('name', 'NO NAME'))+name_add
		def mana_cost(card):
			return str(card.get('manaCost', card.get('colors', '')))
		def types(card):
			return str(card.get('type', ''))
		def oracle(card):
			return str(card.get('text', ''))
		def ptl(card):
			p = card.get('power', '')
			if p: return str(p)+'/'+str(card.get('toughness', ''))
			return str(card.get('loyalty', ''))
		def printings(card):
			return str(card.get('printings', ''))
		def frm_set(card):
			return str(card.get('set', ''))
		def flavors(card):
			return str(card.get('flavors', ''))
		def rarity(card):
			return str(card.get('rarity', ''))
		def space(card):
			return ' '
		switch = {
			'n': name,
			'm': mana_cost,
			't': types,
			'o': oracle,
			'p': ptl,
			'e': printings,
			'x': frm_set,
			'f': flavors,
			'r': rarity,
			's': space
		}
		@staticmethod
		def get(card, s = 'Nmtop'):
			def _get_item(f, card, separator='\n'):
				v = f(card)
				if v:
					return v + separator
				return ''
			return ''.join(
				[
					_get_item(
						Card.CardView.switch.get(k.lower(),
					 	Card.CardView.invalid),
						card,
						' ' if k.isupper() else '\n'
					)
					for k in s
				]
			)
	def view(self, style = 'Nmtop'):
		return Card.CardView.get(self, style)
	def match(self, other):
		return not [
			key
			for key in
			list(self)
			if not key in other
			or not re.match(str(self[key]), str(other[key]), re.IGNORECASE+re.DOTALL)
		]
	def full_name(self):
		return self.get('set', '')+'/'+self.get('name', 'NONAME')
	def printing(self, mset):
		sets = CardLoader.get_sets()
		for card in sets[mset]['cards']:
			if card['name']==self['name']:
				return Card(card)
	def getPrintable(self):
		sets = CardLoader.get_sets()
		for setkey in self['printings']:
			for card in sets[setkey]['cards']:
				if card['name']==self['name'] and 'multiverseid' in card: return Card(card)
	def getThisFromASet(self):
		sets = CardLoader.get_sets()
		fallbackcard = None
		for setkey in self['printings']:
			for card in sets[setkey]['cards']:
				if card['name']==self['name']:
					if 'multiverseid' in card: return Card(card)
					elif not fallbackcard: fallbackcard = Card(card)
		return fallbackcard

		
class NamedCards(object):
	nonpermanentCard = Card({'type': '.*(instant|sorcery).*'})
	creatureCard = Card({'type': '.*creature.*'})
	artifactCard = Card({'type': '.*artifact.*'})
	enchantmentCard = Card({'type': '.*enchantment.*'})
	landCard = Card({'type': '.*land.*'})
	planeswalkerCard = Card({'type': '.*planeswalker.*'})
	instantCard = Card({'type': '.*instant.*'})
	sorceryCard = Card({'type': '.*sorcery.*'})
		
class RealCard(Card):
	def __init__(self, *args, **kwargs):
		super(RealCard, self).__init__(*args, **kwargs)
		if not 'type' in self:
			self['type'] = '.*(instant|sorcery|enchantment|creature|artifact|land|planeswalker).*'
	def match(self, other):
		if 'isFront' in other:
			return other['isFront'] and super(RealCard, self).match(other)
		return super(RealCard, self).match(other)
	
class ReadDeckError(Exception):
	pass

class ReadPoolError(Exception):
	pass

class Deck(object):
	def __init__(self, s='', maindeck = [], sideboard = []):
		self.maindeck = copy.copy(maindeck)
		self.sideboard = copy.copy(sideboard)
		if not s: return
		try:
			Deck.fromXML(s, self)
			return
		except ReadDeckError: pass
		try:
			Deck.fromJson(s, self)
			return
		except ReadDeckError: pass
		Deck.fromString(s, self)
	@staticmethod
	def fromXML(s, deck=None):
		if not deck: deck = Deck()
		try:
			root = ET.fromstring(s)
		except ET.ParseError:
			raise ReadDeckError
		for zone in root.iter('zone'):
			if 'name' in zone.attrib and zone.attrib['name']=='main':
				for card in zone.iter('card'):
					for i in range(int(card.attrib.get('number', 0))):
						if card.attrib['name'] in CardLoader.get_cards():
							deck.maindeck.append(Card.getThisFromASet(CardLoader.get_cards()[card.attrib['name']]))
						else:
							deck.maindeck.append({'name': card.attrib['name']})
			elif 'name' in zone.attrib and zone.attrib['name']=='side':
				for card in zone.iter('card'):
					for i in range(int(card.attrib.get('number', 0))):
						if card.attrib['name'] in CardLoader.get_cards():
							deck.sideboard.append(Card.getThisFromASet(CardLoader.get_cards()[card.attrib['name']]))
						else:
							deck.sideboard.append({'name': card.attrib['name']})
		return deck
	def toXML(self):
		tree = ET.parse(os.path.join(locate.path, 'basedeck.xml'))
		m = tree.find('zone[@name="main"]')
		s = tree.find('zone[@name="side"]')
		for card in set([card['name'] for card in self.maindeck]):
			m.append(
				ET.Element(
					'card',
					{'number': str([card['name'] for card in self.maindeck].count(card)), 'name': card}
				)
			)
		for card in set([card['name'] for card in self.sideboard]):
			s.append(
				ET.Element(
					'card',
					{'number': str([card['name'] for card in self.sideboard].count(card)), 'name': card}
				)
			)
		return tree
	@staticmethod
	def fromString(s, deck=None):
		if not deck: deck = Deck()
		for m in re.finditer('(SB: )?\s*(\d+)?x?\s*(([\w\d\'\-:,]+ ?)+)\s*', s, re.IGNORECASE):
			if m.groups()[1]: amnt = int(m.groups()[1])
			else: amnt = 1
			if not m.groups()[0]:
				for i in range(amnt):
					if m.groups()[2] in CardLoader.get_cards():
						deck.maindeck.append(Card.getThisFromASet(CardLoader.get_cards()[m.groups()[2]]))
					else:
						deck.maindeck.append({'name': m.groups()[2]})
			else:
				for i in range(amnt):
					if m.groups()[2] in CardLoader.get_cards():
						deck.sideboard.append(Card.getThisFromASet(CardLoader.get_cards()[m.groups()[2]]))
					else:
						deck.sideboard.append({'name': m.groups()[2]})
		return deck
	def toString(self):
		maindecknames = [card['name'] for card in self.maindeck]
		sideboardnames = [card['name'] for card in self.sideboard]
		return ''.join([
			str(maindecknames.count(card))+' '+card+'\n'
			for card in set(maindecknames)]
			+['SB: '+str(sideboardnames.count(card))+' '+card+'\n'
			for card in set(sideboardnames)
		])
	@staticmethod
	def fromJson(s, deck=None):
		if not deck: deck = Deck()
		try: jdeck = json.loads(s)
		except json.decoder.JSONDecodeError: 
			raise ReadDeckError
		deck.maindeck = jdeck['main']
		deck.sideboard = jdeck['side']
		return deck
	def toJson(self):
		return json.dumps({'main': self.maindeck, 'side': self.sideboard}, ensure_ascii=False)
	def _75(self):
		return self.maindeck+self.sideboard
	def check(self):
		return checkList([card['name'] for card in self._75()])

class CardList(list):
	def view(self, seperator=', ', style='N'):
		return ''.join([Card.view(card, style)+seperator for card in self])
		
class Pool(CardList):
	def __init__(self, *args, s='', boosters = []):
		super(Pool, self).__init__(*args)
		if s:
			try:
				Pool.fromXML(s, self)
				return
			except ReadDeckError: pass
			try:
				Pool.fromJson(s, self)
				return
			except ReadDeckError: pass
			Pool.fromString(s, self)
			return
		elif boosters:
			for booster in boosters: self.extend(booster)
	@staticmethod
	def fromXML(s, pool=None):
		if pool==None: pool = Pool()
		try: root = ET.fromstring(s)
		except ET.ParseError: raise ReadDeckError
		for zone in root.iter('zone'):
			if 'name' in zone.attrib and zone.attrib['name']=='pool':
				for card in zone.iter('card'):
					for i in range(int(card.attrib.get('number', 0))):
						if card.attrib['name'] in CardLoader.get_cards():
							pool.append(Card.getThisFromASet(CardLoader.get_cards()[card.attrib['name']]))
						else:
							pool.append({'name': card.attrib['name']})
		return pool
	def toXML(self):
		tree = ET.parse(os.path.join(locate.path, 'basepool.xml'))
		p = tree.find('zone[@name="pool"]')
		for card in set([card['name'] for card in self]):
			p.append(ET.Element('card', {'number': str([card['name'] for card in self].count(card)), 'name': card}))
		return tree
	@staticmethod
	def fromString(s, pool=None):
		if pool==None: pool = Pool()
		for m in re.finditer('(SB: )?\s*(\d+)?x?\s*(([\w\d\'\-:,]+ ?)+)\s*', s, re.IGNORECASE):
			if m.groups()[1]: amnt = int(m.groups()[1])
			else: amnt = 1
			for i in range(amnt):
				if m.groups()[2] in CardLoader.get_cards(): pool.append(Card.getThisFromASet(CardLoader.get_cards()[m.groups()[2]]))
				else: pool.append({'name': m.groups()[2]})
		return pool
	def toString(self):
		names = [card['name'] for card in self]
		return ''.join([str(names.count(card))+' '+card+'\n' for card in set(names)])
	@staticmethod
	def fromJson(s, pool=None):
		if pool==None: pool = Pool()
		try: jpool = json.loads(s)
		except json.decoder.JSONDecodeError: raise ReadPoolError
		pool[:] = jpool
		return pool
	def toJson(self):
		return json.dumps(self, ensure_ascii=False)
	def check(self):
		return checkList([card['name'] for card in self])
	
class Selector(tuple):		
	def select(self):
		roll = random.randint(1, sum(e[0] for e in self))
		for pair in self:
			roll -= pair[0]
			if roll<=0: return pair[1]
		raise IndexError
		
def toNestedTuple(lst):
	return tuple(
		toNestedTuple(element)
		if isinstance(element, list) else
		element
		for element in lst
	)
		
class BoosterKey(list):
	common = RealCard({'rarity': 'Common'})
	uncommon = RealCard({'rarity': 'Uncommon'})
	rare = RealCard({'rarity': 'Rare'})
	mythicrare = RealCard({'rarity': 'Mythic Rare'})
	specialrare = RealCard({'rarity': 'Special'})
	doublefacedCommon = RealCard({'rarity': 'Common', 'layout': 'double-faced'})
	doublefacedUncommon = RealCard({'rarity': 'Uncommon', 'layout': 'double-faced'})
	doublefacedRare = RealCard({'rarity': 'Rare', 'layout': 'double-faced'})
	doublefacedMythicrare = RealCard({'rarity': 'Mythic Rare', 'layout': 'double-faced'})
	timeshiftedCommon = RealCard({'rarity': 'Common', 'timeshifted': 'True'})
	timeshiftedUncommon = RealCard({'rarity': 'Uncommon', 'timeshifted': 'True'})
	timeshiftedRare = RealCard({'rarity': 'Rare', 'timeshifted': 'True'})
	timeshiftedMythicrare = RealCard({'rarity': 'Mythic Rare', 'timeshifted': 'True'})
	draftmattersCommon = RealCard({'rarity': 'Common', 'draftmatters': 'True'})
	draftmattersuUncommon = RealCard({'rarity': 'Uncommon', 'draftmatters': 'True'})
	draftmattersRare = RealCard({'rarity': 'Rare', 'draftmatters': 'True'})
	draftmattersMythicrare = RealCard({'rarity': 'Mythic Rare', 'timeshifted': 'True'})
	urzaLand = RealCard({'type': 'land', 'name': 'urza'})
	randomCardStandardWithMythic = Selector(((1, mythicrare), (7, rare), (21, uncommon), (77, common)))
	randomCardStandardWithPower = Selector(((1, specialrare), (53, mythicrare), (371, rare), (1113, uncommon), (4081, common)))
	rareOrMythicStandard = Selector(((1, mythicrare), (7, rare)))
	randomCardTimeShifted = Selector(((1, timeshiftedRare), (3, timeshiftedUncommon), (11, timeshiftedCommon)))
	rareOrTimeshiftedRare = Selector(((1, timeshiftedRare), (7, rare)))
	homelandsUncommonOrRare = Selector(((1, rare), (3, uncommon)))
	eldritchmoondoublefacedOrCommon = Selector(((1, doublefacedMythicrare), (7, doublefacedRare), (49, common)))
	doublefacedCommonOrUncommon = Selector(((3, doublefacedUncommon), (11, doublefacedCommon)))
	stringToPatternMap = {
		'double faced mythic rare': doublefacedMythicrare,
		'double faced uncommon': doublefacedUncommon,
		'foil uncommon': uncommon,
		'double faced common': doublefacedCommon,
		'marketing': None,
		'common': common,
		'checklist': None,
		'double faced rare': doublefacedRare,
		'foil rare': rare,
		'draft-matters': randomCardStandardWithMythic,
		'foil mythic rare': mythicrare, 
		'rare': rare,
		'land': None,
		'timeshifted uncommon': timeshiftedUncommon,
		'uncommon': uncommon,
		'timeshifted common': timeshiftedCommon,
		'urza land': urzaLand,
		'timeshifted rare': timeshiftedRare,
		'power nine': specialrare,
		'mythic rare': mythicrare,
		'foil common': common,
		'timeshifted purple': randomCardTimeShifted
	}
	setToPatternMap = {
		('land', 'checklist'): None,
		('rare', 'timeshifted rare'): rareOrTimeshiftedRare,
		('rare', 'uncommon'): homelandsUncommonOrRare,
		('foil mythic rare', 'foil rare', 'foil uncommon', 'foil common'): randomCardStandardWithMythic,
		('power nine', 'foil'):  randomCardStandardWithPower,
		('common', ('double faced rare', 'double faced mythic rare')): eldritchmoondoublefacedOrCommon,
		('uncommon', 'timeshifted uncommon'): uncommon,
		('common', 'timeshifted common'): common,
		('timeshifted rare', 'timeshifted uncommon'): rare,
		('common', 'double faced rare', 'double faced mythic rare'): eldritchmoondoublefacedOrCommon,
		('double faced common', 'double faced uncommon'): doublefacedCommonOrUncommon,
		('rare', 'mythic rare'): rareOrMythicStandard
	}
	def __init__(self, slots=None, mset=None):
		if isinstance(mset, dict) and 'booster' in mset: self.makeFromList(mset['booster'])
		elif slots: self.makeFromList(slots)
	def makeFromList(self, slots):
		self[:] = [
			self.setToPatternMap[slot]
			if isinstance(slot, tuple) else
			self.stringToPatternMap.get(slot.lower(), RealCard({'rarity': slot}))
			for slot in toNestedTuple(slots)
		]
	def getBoosterMap(self, mset):
		return BoosterMap(mset=mset, key=self)
		
class BoosterMap(list):
	def __init__(self, mset = None, key = None):
		self.fromSet = mset
		if not mset or not key:
			return
		for slot in set(key):
			if isinstance(slot, Selector):
				item = Selector((pair[0], [card for card in mset['cards'] if pair[1].match(card)]) for pair in slot)
			elif slot:
				item = [card for card in mset['cards'] if slot.match(card)]
			else:
				continue
			for i in range(key.count(slot)):
				self.append(item)
	def generate_booster(self, allow_duplicate = False):
		if allow_duplicate:
			return Booster(
				[
					copy.deepcopy(random.choice(option))
						for option in (
							slot.select()
							if isinstance(slot, Selector) else
							slot
							for slot in self
						)
					if option
				], frm_set=self.fromSet
			)
		lst = []
		for slot in self:
			sl = [card for card in
				(slot.select() if isinstance(slot, Selector) else slot)
				if not card in lst
			]
			if sl:
				lst.append(random.choice(sl))
		return Booster(copy.deepcopy(lst), frm_set=self.fromSet)
		
class Booster(CardList):
	def __init__(self, *args, frm_set = None):
		super(Booster, self).__init__(*args)
		self.fromSet = frm_set
	
class MTGSet(dict):
	def __init__(self, *args, **kwargs):
		super(MTGSet, self).__init__(*args, **kwargs)
		self.booster_key = None
		self.booster_map = None
	class SetView(object):
		def invalid(mset):
			return 'INVALID STYLE'
		def name(mset):
			return mset.get('name', 'NO NAME')
		def code(mset):
			return mset.get('code', '')
		def block(mset):
			b = mset.get('block', '')
			if b: b = '('+b+')'
			return b
		def length(mset):
			l = mset.get('cards', '')
			if l: l = len(l)
			return str(l)
		def booster(mset):
			return str(mset.get('booster', ''))
		def space(mset):
			return ' '
		switch = {
			'n': name,
			'c': code,
			'b': block,
			'l': length,
			'o': booster,
			's': space
		}
		@staticmethod
		def get(card, s = 'CNB'):
			def get_item(f, card, seperator='\n'):
				v = f(card)
				if v: return v+seperator
				return ''
			return ''.join([get_item(MTGSet.SetView.switch.get(k.lower(), MTGSet.SetView.invalid), card, ' ' if k.isupper() else '\n') for k in s])
	def view(self, style = 'CNB'):
		return MTGSet.SetView.get(self, style)
	def set_booster_key(self, key=None):
		if key is not None:
			self.booster_key = key
		elif not self.booster_key:
			self.booster_key = BoosterKey(mset=self)
	def get_booster_key(self):
		if self.booster_key is None:
			self.set_booster_key()
		return self.booster_key
	def set_booster_map(self, map=None):
		if map is not None:
			self.booster_map = map
		elif not self.booster_map:
			self.booster_map = self.get_booster_key().getBoosterMap(self)
	def generate_booster(self):
		self.set_booster_map()
		return self.booster_map.generate_booster()
	# def generateCubeBoosterMap(self):
	# 	return CubeBoosterMap(mset=self, key=self.getBoosterKey())
