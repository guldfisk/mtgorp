import re
from mtgUtility import *
from loadCards import *
import terminalsize

trans = {'n': 'name', 'o': 'text', 'c': 'colors', 'p': 'power', 'to': 'toughness', 't': 'type', 'm': 'manaCost', 'cmc': 'cmc', 'e': 'printings', 'f': 'flavors'}

class CardMatch(Card):
	def __init__(self, *args, **kwargs):
		super(CardMatch, self).__init__(*args, **kwargs)
		s = kwargs.get('s', '')
		for ob in re.finditer(r'([^|]*?(\w+)(:|;) *)?([^|]+)', s):
			ud = ob.groups()[3]
			if ob.groups()[2]==':': ud = '.*'+ud+'.*'
			if ob.groups()[1] in trans: self[trans[ob.groups()[1]]] = ud
			else: self['name'] = '.*'+ud+'.*'
				
class CardList(list):
	def __init__(self, *args):
		super(CardList, self).__init__(*args)
		self.head = 0
	def matchList(self, mo):
		return CardList([card for card in self if mo.match(card)])
	def get(self, amnt=1):
		self.head += amnt
		if self.head>len(self): self.head = len(self)-1
		return self[self.head-amnt:self.head]
	def peek(self):
		if not self.head>=len(self)-1: return self[self.head+1]
	def moveHead(self, to):
		self.head = to

class SearchSession(object):
	def __init__(self, cards, ic = input, oc = print):
		self.cards = CardList(sorted(cards, key = lambda card: card['name']))
		self.ic = ic
		self.oc = oc
		self.style = 'nmtop'
		self.cardDivider = '---------------------------------\n\n'
		self.running = False
	def showCards(self, cl):
		s = Card.view(cl.get()[0], self.style)
		while cl.peek() and s.count('\n')+Card.view(cl.peek(), self.style).count('\n')<terminalsize.get_terminal_size()[1]-6-self.cardDivider.count('\n'):
			s += self.cardDivider+Card.view(cl.get()[0], self.style)
		s += self.cardDivider+str(len(cl))+' results, '+str(len(cl)-cl.head)+' remaining'
		self.oc(s)
	def run(self):
		self.running = True
		while self.running:
			cmd = self.ic()
			if cmd=='exit':
				self.running = False
				break
			cl = self.cards.matchList(CardMatch(s=cmd))
			while cl and cl.head<len(cl):
				self.showCards(cl)
				cmd = self.ic()
				if cmd=='q': break
				elif cmd=='exit': 
					self.running = False
					break
				elif cmd: cl = cl.matchList(CardMatch(s=cmd))
				
def main():
	session = SearchSession(CardLoader.getCardsList())
	session.run()
		
if __name__=='__main__': main()