from loadCards import *
import json
from copy import deepcopy
import xml.etree.ElementTree as ET
import re
from collections import OrderedDict
import random

#Adds printings and flavors to allCards.json
def makeCardsFixed():
	cards = deepcopy(CardLoader.getBaseCards())
	sets = CardLoader.getBaseSets()
	for name in cards:
		cards[name]['printings'], cards[name]['flavors'] = getPrintings(name, sets)
		if 'names' in cards[name]: cards[name]['isFront'] = name==cards[name]['names'][0]
	CardWriter.dump(cards, 'cardsFixed.json')
	
def makeSetsFixed():
	sets = deepcopy(CardLoader.getBaseSets())
	for key in sets:
		for card in sets[key]['cards']:
			if 'names' in card: card['isFront'] = card['name']==card['names'][0]
			card['set'] = key
	CardWriter.dump(sets, 'SetsFixed.json')
	
#Gets printings and flavors for a card
def getPrintings(cardName, sets):
	printings = []
	flavors = {}
	for key in sets:
		for card in sets[key]['cards']:
			if card['name']==cardName:
				printings.append(key)
				flavors[key] = card.get('flavor', '')
	return(printings, flavors)

#Returns names from list which are not magic names
def checkList(cards, names=None):
	if names==None: names = CardLoader.getCardsNameList()
	return set([card for card in cards if not card in names])
	
class Card(dict):
	class CardView(object):
		def invalid(card):
			return 'INVALID STYLE'
		def name(card):
			nameAdd = ''
			if card.get('layout', False) == 'split' and 'names' in card and len(card['names'])>1:
				nameAdd = ' // '+[obj for obj in card['names'] if obj!=card['name']][0]
			elif card.get('layout', False) == 'flip' and 'names' in card and len(card['names'])>1:
				nameAdd = '  '+[obj for obj in card['names'] if obj!=card['name']][0]
			elif card.get('layout', False) == 'double-faced' and 'names' in card and len(card['names'])>1:
				nameAdd = ' >> '+[obj for obj in card['names'] if obj!=card['name']][0]
			return str(card.get('name', 'NO NAME'))+nameAdd
		def manaCost(card):
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
		def flavors(card):
			return str(card.get('flavors', ''))
		def space(card):
			return ' '
		switch = {
			'n': name,
			'm': manaCost,
			't': types,
			'o': oracle,
			'p': ptl,
			'e': printings,
			'f': flavors,
			's': space
		}
		@staticmethod
		def get(card, s = 'nmtop'):
			def getItem(f, card, seperator='\n'):
				v = f(card)
				if v: return v+seperator
				return ''
			return ''.join([getItem(Card.CardView.switch.get(k.lower(), Card.CardView.invalid), card, ' ' if k.isupper() else '\n') for k in s])
	def view(self, style = 'nmtop'):
		return Card.CardView.get(self, style)
	def match(self, other):
		return not [key for key in list(self) if not key in other or not re.match(str(self[key]), str(other[key]), re.IGNORECASE+re.DOTALL)]
	def fullName(self):
		return self.get('set', '')+'/'+self.get('name', 'NONAME')

class RealCard(Card):
	def __init__(self, *args, **kwargs):
		super(RealCard, self).__init__(*args, **kwargs)
		if not 'type' in self: self['type'] = 'instant|sorcery|enchantment|creature|artifact|land'
	def match(self, other):
		if 'isFront' in other: return other['isFront'] and super(RealCard, self).match(other)
		return super(RealCard, self).match(other)
		
class ReadDeckError(Exception): pass
		
class Deck(object):
	def __init__(self, s='', maindeck = [], sideboard = []):
		self.maindeck = maindeck
		self.sideboard = sideboard
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
	def fromXML(s, d=None):
		if not d: deck = Deck()
		else: deck = d
		try: root = ET.fromstring(s)
		except ET.ParseError: raise ReadDeckError
		for zone in root.iter('zone'):
			if 'name' in zone.attrib and zone.attrib['name']=='main':
				for card in zone.iter('card'):
					for i in range(int(card.attrib.get('number', 0))): deck.maindeck.append({'name': card.attrib['name']})
			elif 'name' in zone.attrib and zone.attrib['name']=='side':
				for card in zone.iter('card'):
					for i in range(int(card.attrib.get('number', 0))): deck.sideboard.append({'name': card.attrib['name']})
		return deck
	def toXML(self):
		tree = ET.parse('basedeck.xml')
		try:
			m = tree.find('zone[@name="main"]')
			s = tree.find('zone[@name="side"]')
		except ET.ParseError:
			raise ReadDeckError
		for card in set([card['name'] for card in self.maindeck]):
			m.append(ET.Element('card', {'number': str([card['name'] for card in self.maindeck].count(card)), 'name': card}))
		for card in set([card['name'] for card in self.sideboard]):
			s.append(ET.Element('card', {'number': str([card['name'] for card in self.sideboard].count(card)), 'name': card}))
		return tree
	@staticmethod
	def fromString(s, d=None):
		if not d: deck = Deck()
		else: deck = d
		for m in re.finditer('(SB: )?\s*(\d+)?\s*(([\w\d\'-]+ ?)+)\s*', s, re.IGNORECASE):
			if m.groups()[1]: amnt = int(m.groups()[1])
			else: amnt = 1
			if not m.groups()[0]:
				for i in range(amnt): deck.maindeck.append({'name': m.groups()[2]})
			else:
				for i in range(amnt): deck.sideboard.append({'name': m.groups()[2]})
		return deck
	def toString(self):
		maindecknames = [card['name'] for card in self.maindeck]
		sideboardnames = [card['name'] for card in self.sideboard]
		return ''.join([str(maindecknames.count(card))+' '+card+'\n' for card in set(maindecknames)]+['SB: '+str(sideboardnames.count(card))+' '+card+'\n' for card in set(sideboardnames)])
	@staticmethod
	def fromJson(s, d=None):
		if not d: deck = Deck()
		else: deck = d
		try: jdeck = json.loads(s)
		except json.decoder.JSONDecodeError: raise ReadDeckError
		deck.maindeck = jdeck['main']
		deck.sideboard = jdeck['side']
		return deck
	def toJson(self):
		return json.dumps({'main': self.maindeck, 'side': self.sideboard})
	def _75(self):
		return self.maindeck+self.sideboard
	def check(self):
		return checkList([card['name'] for card in self._75()])
		
def toNestedFrozenSet(s):
	return frozenset({toNestedFrozenSet(element) if isinstance(element, list) else element for element in s})
		
def selectFromOrderedDict(d):
	roll = random.randint(1, sum(d))
	for k in d:
		roll -= k
		if roll<=0: return d[k]
	raise IndexError
		
class BoosterKey(list):
	common = RealCard({'rarity': 'Common'})
	uncommon = RealCard({'rarity': 'Uncommon'})
	rare = RealCard({'rarity': 'Rare'})
	mythicrare = RealCard({'rarity': 'Mythic Rare'})
	specialrare = RealCard({'rarity': 'Special'})
	specialrarity = RealCard({'rarity': 'Special'})
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
	randomCardStandardWithMythic = OrderedDict({1: mythicrare, 7: rare, 21: uncommon, 77: common})
	randomCardStandardWithPower = OrderedDict({1: specialrare, 53: mythicrare, 371: rare, 1113: uncommon, 4081: common})
	rareOrMythicStandard = OrderedDict({1: mythicrare, 7: rare})
	randomCardTimeShifted = OrderedDict({1: timeshiftedRare, 3: timeshiftedUncommon, 11: timeshiftedCommon})
	rareOrTimeshiftedRare = OrderedDict({1: timeshiftedRare, 7: rare})
	homelandsUncommonOrRare = OrderedDict({1: rare, 3: uncommon})
	eldritchmoondoublefacedOrCommon = OrderedDict({1: doublefacedMythicrare, 7: doublefacedRare, 49: common})
	doublefacedCommonOrUncommon = OrderedDict({3: doublefacedUncommon, 11: doublefacedCommon})
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
		toNestedFrozenSet({'land', 'checklist'}): None,
		toNestedFrozenSet({'rare', 'timeshifted rare'}): rareOrTimeshiftedRare,
		toNestedFrozenSet({'rare', 'uncommon'}): homelandsUncommonOrRare,
		toNestedFrozenSet({'foil mythic rare', 'foil rare', 'foil uncommon', 'foil common'}): randomCardStandardWithMythic,
		toNestedFrozenSet({'power nine', 'foil'}):  randomCardStandardWithPower,
		toNestedFrozenSet({'common', frozenset({'double faced rare', 'double faced mythic rare'})}): eldritchmoondoublefacedOrCommon,
		toNestedFrozenSet({'uncommon', 'timeshifted uncommon'}): uncommon,
		toNestedFrozenSet({'common', 'timeshifted common'}): common,
		toNestedFrozenSet({'timeshifted rare', 'timeshifted uncommon'}): rare,
		toNestedFrozenSet({'common', 'double faced rare', 'double faced mythic rare'}): eldritchmoondoublefacedOrCommon,
		toNestedFrozenSet({'double faced common', 'double faced uncommon'}): doublefacedCommonOrUncommon,
		toNestedFrozenSet({'rare', 'mythic rare'}): rareOrMythicStandard
	}
	def __init__(self, *args, mset=None):
		super(BoosterKey, self).__init__(*args)
		if isinstance(mset, dict) and 'booster' in mset: self[:] = mset['booster']
		for i in range(len(self)):
			if isinstance(self[i], list): self[i] = self.setToPatternMap[toNestedFrozenSet(self[i])]
			elif isinstance(self[i], str): self[i] = self.stringToPatternMap[self[i]]
			elif not isinstance(self[i], OrderedDict): raise TypeError
	def getBoosterMap(self, mset):
		return BoosterMap(mset=mset, key=self)
		
class BoosterMap(list):
	def __init__(self, *args, mset = None, key = None):
		super(BoosterMap, self).__init__(*args)
		if not mset or not key: return
		self[:] = [
			OrderedDict((k, [card for card in mset['cards'] if slot[k].match(card)]) for k in slot)
			if isinstance(slot, OrderedDict) else
			[card for card in mset['cards'] if slot.match(card)]
			for slot in key if slot
		]
	def getBooster(self, allowDuplicate = False):
		if allowDuplicate: return Booster([
			deepcopy(random.choice(
				selectFromOrderedDict(slot)
				if isinstance(slot, OrderedDict) else
				slot
			))
			for slot in self
		])
		booster = Booster()
		for slot in self:
			sl = [card for card in
				(selectFromOrderedDict(slot) if isinstance(slot, OrderedDict) else slot)
				if not card['name'] in [c['name'] for c in booster]
			]
			if sl: booster.append(deepcopy(random.choice(sl)))
		return booster
		
class Booster(list):
	def view(self, seperator=', ', style='N'):
		return ''.join([Card.view(card, style)+seperator for card in self])
	
class MTGSet(dict):
	def __init__(self, *args, **kwargs):
		super(MTGSet, self).__init__(*args, **kwargs)
		self.boosterkey = None
		self.boostermap = None
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
			def getItem(f, card, seperator='\n'):
				v = f(card)
				if v: return v+seperator
				return ''
			return ''.join([getItem(MTGSet.SetView.switch.get(k.lower(), MTGSet.SetView.invalid), card, ' ' if k.isupper() else '\n') for k in s])
	def view(self, style = 'CNB'):
		return MTGSet.SetView.get(self, style)
	def setBoosterKey(self, key=None):
		if key==None: self.boosterkey = BoosterKey(mset=self)
		else: self.boosterkey = BoosterKey(key)
	def setBoosterMap(self, map=None):
		if self.boosterkey==None: self.setBoosterKey()
		if map==None: self.boostermap = self.boosterkey.getBoosterMap(self)
		else: self.boostermap = map
	def generateBooster(self):
		self.setBoosterMap()
		return self.boostermap.getBooster()

def getKeys(sets):
	s = set()
	for key in sets:
		for card in sets[key]['cards']: s = s.union(list(card))
	return s
	
def getKeyValues(sets, k):
	s = set()
	for key in sets:
		for card in sets[key]['cards']:
			if k in card:
				s.add(str(card[k]))
	return s
	
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])
	
def test():
	
	#deck = Deck(open('deck.txt', 'r').read())
	ss = toNestedFrozenSet({'common', frozenset({'double faced rare', 'double faced mythic rare'})})
	sets = CardLoader.getSets()
	rs = set()
	for key in sets:
		#if 'booster' in sets[key]: print(BoosterKey(sets[key]['booster']))
		if ('booster' in sets[key] and ss in toNestedFrozenSet(sets[key]['booster'])):
			print('------------------')
			print(MTGSet.view(sets[key], 'CNBsO'))
			mset = MTGSet(sets[key])
			bk = BoosterKey(mset=sets[key])
			print(type(bk))
			bm = bk.getBoosterMap(sets[key])
			print(type(bm))
			#booster = bm.getBooster()
			booster = mset.generateBooster()
			print('>>BOOSTER<<', booster.view())
		if 'booster' in sets[key] and 'timeshifted purple' in toNestedFrozenSet(sets[key]['booster']):
			print('*'*20)
			print(MTGSet.view(sets[key], 'CNBsO'))
		if 'booster' in sets[key]:
			rs = rs.union(set(flatten(sets[key]['booster'])))
			if 'urza land' in flatten(sets[key]['booster']): print(MTGSet.view(sets[key], 'CNBsO'))
	print('------------------')	
	print(rs)
	futcard = sets['FUT']['cards']
	
	for rarity in ('Common', 'Uncommon', 'Rare'):
		print(rarity)
		print(len([card for card in futcard if card['rarity']==rarity]))
		print(len([card for card in futcard if card['rarity']==rarity and 'timeshifted' in card]))
	print(rs)
	print(getKeys(sets))
	print(getKeyValues(sets, 'rarity'))
	concard = sets['EMN']['cards']
	print([card for card in concard if card['name']=='Lone Rider'][0])
		
if __name__=='__main__':
	test()