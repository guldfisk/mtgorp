import terminalsize

import tools.cardSearch as cs
from models.mtgObjects import Card
from resourceload.cardload import CardLoader

class SearchSession(object):
	def __init__(self, cards, ic = input, oc = print):
		self.cards = cs.CardList(sorted(cards, key = lambda card: card['name']))
		self.ic = ic
		self.oc = oc
		self.style = 'nmtop'
		self.cardDivider = '---------------------------------\n\n'
		self.running = False
	def show_cards(self, cl):
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
			cl = self.cards.matchList(cs.CardMatch(cmd))
			while cl and cl.head<len(cl):
				self.show_cards(cl)
				cmd = self.ic()
				if cmd=='q': break
				elif cmd=='exit': 
					self.running = False
					break
				elif cmd: cl = cl.matchList(cs.CardMatch(cmd))

def main():
	session = SearchSession(CardLoader.get_cards_list())
	session.run()
		
if __name__=='__main__':
	main()