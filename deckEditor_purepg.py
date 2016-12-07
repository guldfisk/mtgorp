from pygame import *
import sys
import math as m
import time
from mtgUtility import *
import cardSearch
import time
import threading
from loadImgs import *
from loadCards import *
from fullEvent import *
import numpy as np
import copy

init()

MD = (55, 255, 155)

class DEImageLoader(ImageLoader):
	imageNameFont = font.Font(None, 30)
	def _loadImage(self, path, name, card):
		with open(path, 'rb') as f:
			full = image.load(path)
			half = transform.scale(full, (int(full.get_width()/2), int(full.get_height()/2)))
			color = card.getImageColor()
			nameText = self.imageNameFont.render(card.get('name', 'Default'), 1, color, tuple(255-channel for channel in color))
			if half.get_width()<nameText.get_width(): nameText = transform.scale(nameText, (half.get_width(), nameText.get_height()))
			half.blit(nameText, nameText.get_rect())
			self.images[name+'_full'] = full
			self.images[name] = half

class DECard(object):
	def __init__(self, session, d):
		self.session = session
		if not 'set' in d and 'printings' in d: d = Card.getThisFromSet(d, d['printings'][0])
		self.d = Card(d)
		self.rekt = self.session.imageLoader.getImage(self.d).get_rect()
	def draw(self):
		self.session.screen.blit(self.session.imageLoader.getImage(self.d), self.rekt)
		if self in self.session.selected: draw.rect(self.session.screen, (255, 0, 0), self.rekt, 3)
	def move(self, x, y):
		self.session.upToDate = False
		self.rekt.move_ip(x, y)
		self.rekt.clamp_ip(Rect((0, 0), self.session.getSize()))
	def moveTo(self, x, y):
		self.session.upToDate = False
		self.rekt.x, self.rekt.y = x, y
		self.rekt.clamp_ip(Rect((0, 0), self.session.getSize()))
		
class Stack:
	def __init__(self, session, pos = (0, 0), dim = (100, 100)):
		self.session = session
		self.cards = []
		self.spread = 40
		self.baserekt = self.session.imageLoader.getDefault().get_rect()
		self.rekt = Rect(pos, dim)
	def move(self, x, y):
		self.rekt.move_ip(x, y)
		self.alignAll()
	def moveTo(self, x, y):
		self.rekt.x, self.rekt.y = x, y
		self.alignAll()
	def resize(self, x, y, w, h):
		self.rekt.w, self.rekt.h = w, h
		self.moveTo(x, y)
	# def alignCard(self, card):
		# card.moveTo(self.rekt[0], self.rekt[1]+self.spread*(len(self.cards)-1))
	def alignAll(self):
		for i in range(len(self.cards)): self.cards[i].moveTo(self.rekt[0], self.rekt[1]+(i)*max(self.rekt.h-self.cards[i].rekt.h, 0)/len(self.cards))
	def put(self, card):
		self.cards.append(card)
		self.alignAll()
	def take(self, card):
		i = 0
		while i<len(self.cards):
			if card==self.cards[i]:
				del self.cards[i]
				break
			i += 1
		self.alignAll()
			
class StackAlign(Stack):
	def __init__(self, session, pos=np.zeros((2))):
		super(StackAlign, self).__init__(session, pos)
		self.session.connectCondition(Replacement, trigger='PickupCard', source=self, resolve=self.resolvePickup, condition=self.conditionPickup)
		self.session.connectCondition(Replacement, trigger='DropCard', source=self, resolve=self.resolveDrop, condition=self.conditionDrop)
	def conditionPickup(self, **kwargs):
		return kwargs['card'] in self.cards
	def resolvePickup(self, event, **kwargs):
		self.take(event.card)
		event.spawnClone().resolve()
	def conditionDrop(self, **kwargs):
		return self.rekt.collidepoint(kwargs['pos'])
	def resolveDrop(self, event, **kwargs):
		self.put(event.card)
		event.spawnClone().resolve()
	
class UIElement(object):
	def __init__(self, session):
		self.session = session
		self.session.uielements.append(self)
	def draw(self):
		raise NotImplemented
		
class SelectionBox(UIElement):
	def __init__(self, session, anchor = (0, 0), color = (0, 0, 200)):
		super(SelectionBox, self).__init__(session)
		self.anchor = np.array(anchor)
		self.corner = np.array(anchor)
		self.pos = [0, 0]
		self.dim = [0, 0]
		self.s = None
		self.newSurface()
		self.color = color
	def newSurface(self):
		for i in range(2):
			if self.anchor[i]<self.corner[i]:
				self.pos[i] = self.anchor[i]
				self.dim[i] = self.corner[i]-self.anchor[i]
			else:
				self.pos[i] = self.corner[i]
				self.dim[i] = self.anchor[i]-self.corner[i]
		self.s = Surface(self.dim)
		self.s.set_alpha(128)
		self
	def resize(self, rel):
		self.corner += np.array(rel)
		self.newSurface()
	def draw(self):
		self.session.screen.blit(self.s, self.pos)
	def end(self):
		colrek = Rect(self.pos, self.dim)
		self.session.updateSelected(*set(card for card in self.session.cards if card.rekt.colliderect(colrek)))
		self.session.uielements.remove(self)
		
class PickupCards(Event):
	name = 'PickupCards'
	def check(self, **kwargs):
		pass
	def payload(self, **kwargs):
		self.session.floatingStack = Stack(self.session, self.pos)
		for card in self.cards: self.spawn(PickupCard, card=card).resolve()
		
class PickupCard(Event):
	name = 'PickupCard'
	def payload(self, **kwargs):
		self.session.moveCardsToFront(self.card)
		self.session.floatingStack.put(self.card)
		
class DropCards(Event):
	name = 'DropCards'
	def payload(self, **kwargs):
		self.session.floatingStack = None
		for card in self.cards: self.spawn(DropCard, card=card).resolve()
		
class DropCard(Event):
	name = 'DropCard'
	def payload(self, **kwargs):
		pass
			
POINTCLICK = USEREVENT+1
		
class UIBehaviour(object):
	def __init__(self, session):
		self.session = session
	def feed(self, pevent):
		raise NotImplemented
	def draw(self):
		pass
		
class PointCick(UIBehaviour):
	def __init__(self, session):
		super(PointCick, self).__init__(session)
		self.lastdown = None
	def feed(self, pevent):
		if pevent.type==MOUSEBUTTONDOWN and pevent.button==1:
			self.lastdown = pevent.pos
		elif pevent.type==MOUSEBUTTONUP and pevent.button==1 and self.lastdown:
			if pevent.pos==self.lastdown: event.post(event.Event(POINTCLICK, {'pos': pevent.pos}))

class Deselect(UIBehaviour):
	def __init__(self, session):
		super(Deselect, self).__init__(session)
		self.selectionbox = None
	def feed(self, pevent):
		if pevent.type==POINTCLICK and not self.session.getTopCollision(pevent.pos):
			self.session.selected.clear()
			
class SingleSelect(UIBehaviour):
	def __init__(self, session):
		super(SingleSelect, self).__init__(session)
		self.selectionbox = None
	def feed(self, pevent):
		if pevent.type==POINTCLICK:
			card = self.session.getTopCollision(pevent.pos)
			if card: self.session.updateSelected(card)
		elif pevent.type==MOUSEBUTTONDOWN and pevent.button==1:
			card = self.session.getTopCollision(pevent.pos)
			if card and not card in self.session.selected:
				self.session.updateSelected(card)
		
class BoxSelect(UIBehaviour):
	def __init__(self, session):
		super(BoxSelect, self).__init__(session)
		self.selectionbox = None
	def feed(self, pevent):
		if pevent.type==MOUSEBUTTONDOWN and pevent.button==1 and not self.session.getTopCollision(pevent.pos):
			self.selectionbox = SelectionBox(self.session, pevent.pos)
		elif pevent.type==MOUSEMOTION and pevent.buttons[0] and self.selectionbox:
			self.selectionbox.resize(pevent.rel)
		elif pevent.type==MOUSEBUTTONUP and pevent.button==1 and self.selectionbox:
			self.selectionbox.end()
			self.selectionbox = None

class MoveSelected(UIBehaviour):
	def feed(self, pevent):
		if pevent.type==MOUSEBUTTONDOWN and pevent.button==1:
			card = self.session.getTopCollision(pevent.pos)
			if card and card in self.session.selected:
				self.session.resolveEvent(PickupCards, cards=self.session.selected, pos=pevent.pos)
		elif pevent.type==MOUSEMOTION and pevent.buttons[0] and self.session.floatingStack and self.session.selected:
			for card in self.session.selected: card.move(*pevent.rel)
		elif pevent.type==MOUSEBUTTONUP and pevent.button==1 and self.session.floatingStack:
			self.session.resolveEvent(DropCards, cards=self.session.selected, pos=pevent.pos)
		
class HoverView(UIBehaviour):
	def __init__(self, session):
		super(HoverView, self).__init__(session)
		self.showcase = None
	def feed(self, pevent):
		if pevent.type==MOUSEMOTION:
			self.showcase = self.session.getTopCollision(pevent.pos)
	def draw(self):
		if not self.showcase: return
		img = self.session.imageLoader.images.get(self.showcase.d.fullName()+'_full', None)
		if not img: return
		rekt = img.get_rect()
		self.session.screen.blit(img, (self.session.getSize()[0]-rekt.w, 0, rekt.w, rekt.h))
		
class CardAdder(UIBehaviour):
	textFont = font.Font(None, 50)
	textForegroundColor = (255, 255, 255)
	textBeckgroundColor = (0, 0, 0)
	def __init__(self, session):
		super(CardAdder, self).__init__(session)
		self.text = ''
		self.hits = None
		self.cards = cardSearch.CardList(sorted(CardLoader.getCardsList(), key = lambda card: card['name']))
	def feed(self, pevent):
		if pevent.type==KEYDOWN:
			if pevent.key==13:
				if self.hits: self.session.addCards(self.hits.get()[0])
				self.text = ''
				self.hits = None
			elif pevent.key==273 and self.hits:
				self.hits.moveHead(-1)
			elif pevent.key==274 and self.hits:
				self.hits.moveHead(1)
			else:
				if pevent.key==8:
					self.text = self.text[:-1]
				else: self.text += pevent.unicode
				self.hits = self.cards.matchList(cardSearch.CardMatch(self.text))
	def draw(self):
		if not self.text: return
		img = self.textFont.render(self.text, 1, self.textForegroundColor, self.textBeckgroundColor)
		self.session.screen.blit(img, (0, 0))
		if not self.hits: return
		peeked = self.hits.peekMultiple(10)
		for i in range(len(peeked)):
			img = self.textFont.render(Card.view(peeked[i], 'N'), 1, self.textForegroundColor, self.textBeckgroundColor)
			self.session.screen.blit(img, (0, self.textFont.size('a')[1]*(i+1)))
			
class DeckEditorSession(EventSession):
	def __init__(self, size = (1200, 600), **kwargs):
		super(DeckEditorSession, self).__init__(**kwargs)
		self.cards = []
		self.stacks = []
		self.size = size
		self.floatingStack = None
		self.selected = set()
		self.upToDate = False
		self.imageLoader = DEImageLoader()
		self.running = False
		self.uielements = []
		self.selectionbox = None
		self.uibehaviour = [PointCick(self), Deselect(self), SingleSelect(self), BoxSelect(self), MoveSelected(self), HoverView(self), CardAdder(self)]
		self.screen = None
		self.grid = (10, 2)
		self.makeStacks(*self.grid)
	def getSize(self):
		if self.screen: return self.screen.get_size()
		return self.size
	def makeStacks(self, columns=5, rows=2):
		if not self.stacks:
			for i in range(rows*columns): self.stacks.append(StackAlign(self))
		s = self.getSize()
		for r in range(rows):
			for c in range(columns):
				self.stacks[r*columns+c].resize(
					s[0]*c/columns,
					0 if r==0 else (self.stacks[(r-1)*columns].rekt.y+s[1]*2**(rows-r)/(2**(rows)-1)),
					s[0]/columns,
					s[1]*2**(rows-r-1)/(2**(rows)-1)
				)
	def moveCardsToFront(self, *cards):
		for card in cards:
			if card in self.cards:
				self.cards.remove(card)
				self.cards.append(card)
	def updateSelected(self, *cards):
		keys = key.get_pressed()
		if keys[K_LSHIFT] and keys[K_LALT]: self.selected.intersection_update(cards)
		elif keys[K_LSHIFT]: self.selected.update(cards)
		elif keys[K_LALT]: self.selected.difference_update(cards)
		else:
			self.selected.clear()
			self.selected.update(cards)
	def getTopCollision(self, point):
		for i in range(len(self.cards)-1, -1, -1):
			if self.cards[i].rekt.collidepoint(point): return self.cards[i]
		return None
	def newWindow(self, w, h):
		self.screen = display.set_mode((w, h), RESIZABLE)
		self.makeStacks(*self.grid)
		self.upToDate = False
	def updateWindow(self):
		if self.upToDate: return
		self.screen.fill(MD)
		for card in self.cards: card.draw()
		# for stack in self.stacks: draw.rect(self.screen, (0, 0, 0), stack.rekt, 3)
		for behaviour in self.uibehaviour: behaviour.draw()
		for uie in self.uielements: uie.draw()
		display.flip()
	def addCards(self, *cards, pos = (0, 0)):
		cards = list(DECard(self, card) for card in cards)
		self.cards.extend(cards)
		self.resolveEvent(DropCards, cards=cards, pos=pos)
	def run(self):
		self.newWindow(*self.size)
		self.running = True
		while self.running:
			pevent = event.wait()
			if pevent.type==QUIT: self.running = False
			elif pevent.type==VIDEORESIZE: self.newWindow(pevent.w, pevent.h)
			elif pevent.type==VIDEOEXPOSE: self.upToDate = False
			elif pevent.type==MOUSEBUTTONDOWN: pass
			for behaviour in self.uibehaviour: behaviour.feed(pevent)
			self.updateWindow()
		
def test():
	
	session = DeckEditorSession()
	set = MTGSet(CardLoader.getSets()['KLD'])
	booster = set.generateBooster()
	for card in booster: print(Card.view(card, 'N'))
	session.addCards(*booster)
	session.run()
	
if __name__=='__main__': test()