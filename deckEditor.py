import pygame
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

pygame.init()

bgcolor = (100, 200, 255)
spread = 17
cSize = (223, 310)

opdeling = (10, 2)

MD = (55, 255, 155)
SB = (100, 200, 255)

class DEImageLoader(ImageLoader):
	def _loadImage(self, path, name):
		with open(path, 'rb') as f:
			full = pygame.image.load(path)
			half = pygame.transform.scale(full, (int(full.get_width()/2), int(full.get_height()/2)))
			self.images[name+'_full'] = full
			self.images[name] = half

class DECard(object):
	def __init__(self, session, d):
		self.session = session
		self.d = Card(d)
		self.rekt = self.session.imageLoader.getImage(self.d).get_rect()
	def draw(self):
		#self.rekt.move(1, 1)
		#print(self.rekt)
		self.session.screen.blit(self.session.imageLoader.getImage(self.d), self.rekt)
		if self in self.session.selected: pygame.draw.rect(self.session.screen, (255, 0, 0), self.rekt, 3)
	def move(self, x, y):
		self.session.upToDate = False
		self.rekt.move_ip(x, y)
		self.rekt.clamp_ip(pygame.Rect((0, 0), self.session.getSize()))
	def moveTo(self, x, y):
		self.session.upToDate = False
		self.rekt.x, self.rekt.y = x, y
		self.rekt.clamp_ip(pygame.Rect((0, 0), self.session.getSize()))
		
class Stack:
	def __init__(self, session, pos = (0, 0), dim = (100, 100)):
		self.session = session
		self.cards = []
		self.spread = 40
		self.baserekt = self.session.imageLoader.getDefault().get_rect()
		self.rekt = pygame.Rect(pos, dim)
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
		self.s = pygame.Surface(self.dim)
		self.s.set_alpha(128)
		self
	def resize(self, rel):
		self.corner += np.array(rel)
		self.newSurface()
	def draw(self):
		self.session.screen.blit(self.s, self.pos)
	def end(self):
		colrek = pygame.Rect(self.pos, self.dim)
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
			
POINTCLICK = pygame.USEREVENT+1
		
class UIBehaviour(object):
	def __init__(self, session):
		self.session = session
	def feed(self, event):
		raise NotImplemented
		
class PointCick(UIBehaviour):
	def __init__(self, session):
		super(PointCick, self).__init__(session)
		self.lastdown = None
	def feed(self, event):
		if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
			self.lastdown = event.pos
		elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and self.lastdown:
			if event.pos==self.lastdown: pygame.event.post(pygame.event.Event(POINTCLICK, {'pos': event.pos}))

class Deselect(UIBehaviour):
	def __init__(self, session):
		super(Deselect, self).__init__(session)
		self.selectionbox = None
	def feed(self, event):
		if event.type==POINTCLICK and not self.session.getTopCollision(event.pos):
			self.session.selected.clear()
			
class SingleSelect(UIBehaviour):
	def __init__(self, session):
		super(SingleSelect, self).__init__(session)
		self.selectionbox = None
	def feed(self, event):
		if event.type==POINTCLICK:
			card = self.session.getTopCollision(event.pos)
			if card: self.session.updateSelected(card)
		elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
			card = self.session.getTopCollision(event.pos)
			if card and not card in self.session.selected:
				self.session.updateSelected(card)
		
class BoxSelect(UIBehaviour):
	def __init__(self, session):
		super(BoxSelect, self).__init__(session)
		self.selectionbox = None
	def feed(self, event):
		if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and not self.session.getTopCollision(event.pos):
			self.selectionbox = SelectionBox(self.session, event.pos)
		elif event.type==pygame.MOUSEMOTION and event.buttons[0] and self.selectionbox:
			self.selectionbox.resize(event.rel)
		elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and self.selectionbox:
			self.selectionbox.end()
			self.selectionbox = None

class MoveSelected(UIBehaviour):
	def __init__(self, session):
		super(MoveSelected, self).__init__(session)
		self.moving = None
	def feed(self, event):
		if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
			card = self.session.getTopCollision(event.pos)
			if card and card in self.session.selected:
				self.session.resolveEvent(PickupCards, cards=self.session.selected, pos=event.pos)
		elif event.type==pygame.MOUSEMOTION and event.buttons[0] and self.session.floatingStack and self.session.selected:
			for card in self.session.selected: card.move(*event.rel)
		elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and self.session.floatingStack:
			self.session.resolveEvent(DropCards, cards=self.session.selected, pos=event.pos)	
		
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
		self.uibehaviour = [PointCick(self), Deselect(self), SingleSelect(self), BoxSelect(self), MoveSelected(self)]
		self.screen = None
		self.grid = (10, 2)
	def getSize(self):
		if self.screen: return self.screen.get_size()
		return self.size
	def makeStacks(self, columns=5, rows=2):
		print('making stacks')
		if not self.stacks:
			for i in range(rows*columns): self.stacks.append(StackAlign(self))
		s = self.getSize()
		for r in range(rows):
			for c in range(columns):
				print(r*columns+c)
				print(2**(rows-r), 0 if r==0 else (self.stacks[(r-1)*columns].rekt.y+2**(rows-r)))
				self.stacks[r*columns+c].resize(
					s[0]*c/columns,
					0 if r==0 else (self.stacks[(r-1)*columns].rekt.y+s[1]*2**(rows-r)/(2**(rows)-1)),
					s[0]/columns,
					s[1]*2**(rows-r-1)/(2**(rows)-1)
				)
				print(self.stacks[r*columns+c].rekt)
	def moveCardsToFront(self, *cards):
		for card in cards:
			if card in self.cards:
				self.cards.remove(card)
				self.cards.append(card)
	def updateSelected(self, *cards):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LSHIFT] and keys[pygame.K_LALT]: self.selected.intersection_update(cards)
		elif keys[pygame.K_LSHIFT]: self.selected.update(cards)
		elif keys[pygame.K_LALT]: self.selected.difference_update(cards)
		else:
			self.selected.clear()
			self.selected.update(cards)
	def getTopCollision(self, point):
		for i in range(len(self.cards)-1, -1, -1):
			if self.cards[i].rekt.collidepoint(point): return self.cards[i]
		return None
	def newWindow(self, w, h):
		self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.makeStacks(*self.grid)
		self.upToDate = False
	def updateWindow(self):
		if self.upToDate: return
		self.screen.fill(MD)
		for card in self.cards: card.draw()
		for stack in self.stacks:
			col = 255-int(255/(len(stack.cards)+1))
			pygame.draw.rect(self.screen, (col, col, col), stack.rekt, 3)
		for uie in self.uielements: uie.draw()
		pygame.display.flip()
	def run(self):
		self.newWindow(*self.size)
		self.running = True
		while self.running:
			event = pygame.event.wait()
			if event.type==pygame.QUIT: self.running = False
			elif event.type==pygame.VIDEORESIZE: self.newWindow(event.w, event.h)
			elif event.type==pygame.VIDEOEXPOSE: self.upToDate = False
			elif event.type==pygame.MOUSEBUTTONDOWN: pass
			for behaviour in self.uibehaviour: behaviour.feed(event)
			self.updateWindow()
		
def dummyEvent():
	global updt
	updt = False
	pygame.event.post(pygame.event.Event(pygame.USEREVENT))

def getHover(pos):
	r = None
	for i in range(len(cards)-1, -1, -1):
		if cards[i].isWithin(pos):
			r = cards[i]
			break
	return(r)
			
def clicked(pos):
	global active
	for i in range(len(cards)-1, -1, -1):
		if cards[i].isWithin(pos):
			cards.append(cards.pop(i))
			active = cards[-1]
			break
		
def getCards():
	md = []
	sb = []
	for c in cards:
		if c.rpos[0]>size[0]/2:
			sb.append(c.name)
		else:
			md.append(c.name)
	return((md, sb))
		
cards = []

def mcards(cards):
	for c in cards:
		cards.append(card(path=c, name=c))

def getPos(n, amnt):
	xdim = int(223/2)
	ydim = m.floor(size[1]/m.floor(amnt/(size[0]/xdim)))
	return([n//m.floor(size[1]/ydim)*xdim, n%m.floor(size[1]/ydim)*ydim])
		
stacks = []

def makeStacks():
	for i in range(m.floor(size[0]/cSize[0])):
		stacks.append(stack((i*cSize[0], 0)))
		
def toStack(c):
	for s in stacks:
		if s.getSize().collidepoint(c.rpos):
			s.put(c)
		
def start(cinds):
	makeStacks()
	if type(cinds[0]) is dict:
		for i in range(len(cinds)):
			#stacks[i%len(stacks)].put(card(path=cinds[i]['set']+'\\'+cinds[i]['name'], name=cinds[i]['name']))
			#toStack(card(path=cinds[i]['set']+'\\'+cinds[i]['name'], name=cinds[i]['name']))
			cards.append(card(path=cinds[i]['set']+'\\'+cinds[i]['name'], name=cinds[i]['name'], rpos=getPos(i, len(cinds))))
	main()
		
def main():
	global active
	global updt
	global run
	global hoverTime
	currentHover = None
	while run:
		event = pygame.event.wait()
		print(event)
		if event.type==pygame.QUIT:
			run = False
		elif event.type==pygame.MOUSEBUTTONDOWN:
			clicked(pygame.mouse.get_pos())
		elif event.type==pygame.MOUSEBUTTONUP:
			if active:
				active.snap()
			active = None
		elif event.type==pygame.MOUSEMOTION:
			if active:
				active.move(event.rel)
		elif event.type==pygame.KEYDOWN and event.key==pygame.K_u:
			cs = getCards()
			codder.save(time.strftime("deckeditor\\Draft_%d_%m_%Y_%H_%M_%S"), *cs)
		newHover = getHover(pygame.mouse.get_pos())
		if not currentHover == newHover and newHover:
			currentHover = newHover
			updt = False		
			hoverTime = time.time()
			hT = threading.Timer(popUpDelay+0.1, dummyEvent)
			hT.start()
		if not updt:
			screen.fill(MD, pygame.Rect(0, 0, m.ceil(size[0]/2), size[1]))
			screen.fill(SB, pygame.Rect(m.ceil(size[0]/2), 0, m.ceil(size[0]/2), size[1]))
			for c in cards:
				c.draw()
			if currentHover and not active and time.time()>hoverTime+popUpDelay:
				currentHover.orekt.x, currentHover.orekt.y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
				screen.blit(currentHover.oimg, currentHover.orekt)
			pygame.display.flip()
			updt = True
		
def test():
	session = DeckEditorSession()
	set = MTGSet(CardLoader.getSets()['ZEN'])
	booster = set.generateBooster()
	for i in range(len(booster)):
		card = DECard(session, booster[i])
		card.move(50*i, 25*i)
		print(card.d.view('N'))
		session.cards.append(card)
	session.run()
	
		
if __name__=='__main__': test()