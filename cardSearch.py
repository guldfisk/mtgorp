import re
from mtgUtility import *
from loadCards import *

class CardMatch(Card):
	trans = {
		'n': 'name',
		'o': 'text',
		'c': 'colors',
		'p': 'power',
		'to': 'toughness',
		't': 'type',
		'm': 'manaCost',
		'cmc': 'cmc',
		'e': 'printings',
		'f': 'flavors'
	}
	def __init__(self, *args, **kwargs):
		super(CardMatch, self).__init__(**kwargs)
		if len(args)>0: s = args[0]
		else: s = ''
		for ob in re.finditer(r'([^|]*?(\w+)(:|;) *)?([^|]+)', s):
			ud = ob.groups()[3]
			if ob.groups()[2]==':': ud = '.*'+ud+'.*'
			if ob.groups()[1] in self.trans: self[self.trans[ob.groups()[1]]] = ud
			else: self['name'] = '.*'+ud+'.*'

class CardList(list):
	def __init__(self, *args):
		super(CardList, self).__init__(*args)
		self.head = 0
	def matchList(self, mo):
		lst = CardList([card for card in self if mo.match(card)])
		return lst
	def get(self, amnt=1):
		self.head += amnt
		if self.head>len(self): self.head = len(self)-1
		return self[self.head-amnt:self.head]
	def peek(self):
		if not self.head>=len(self)-1: return self[self.head+1]
	def moveHead(self, to):
		self.head = to