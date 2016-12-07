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
import embedableSurface
from PyQt5 import QtWidgets, QtGui, QtCore
import pickle

font.init()

class DEImageLoader(ImageLoader):
	imageNameFont = font.Font(None, 30)
	def _loadImage(self, path, name, card):
		with open(path, 'rb') as f:
			full = image.load(path)
			half = transform.scale(full, (int(full.get_width()/2), int(full.get_height()/2)))
			color = card.getImageColor()
			nameText = self.imageNameFont.render(card.get('name', 'Default'), 1, color, tuple(max(channel-155, 0) for channel in color))
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
	def draw(self, surface):
		surface.blit(self.session.imageLoader.getImage(self.d), self.rekt)
		if self in self.session.selected: draw.rect(surface, (255, 0, 0), self.rekt, 3)
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
	def draw(self, surface):
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
	def resizeTo(self, pos):
		self.corner = np.array(pos)
		self.newSurface()
	def resize(self, rel):
		self.corner += rel
		self.newSurface()
	def draw(self, surface):
		surface.blit(self.s, self.pos)
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
			
class MultiCardWidget(embedableSurface.EmbeddedSurface, EventSession):
	def __init__(self, **kwargs):
		super(MultiCardWidget, self).__init__(**kwargs)
		self.cards = []
		self.stacks = []
		self.floatingStack = None
		self.selectionbox = None
		self.selected = set()
		self.imageLoader = kwargs.get('imageloader', DEImageLoader())
		self.uielements = []
		self.selectionbox = None
		self.grid = (10, 2)
		self.makeStacks(*self.grid)
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.contextMenu)
	def contextMenu(self, pos):
		menu = QtWidgets.QMenu()
		subMenu = QtWidgets.QMenu(':)')
		wauwAction = subMenu.addAction('wauw')
		quitAction = menu.addAction("Quit")
		menu.addMenu(subMenu)
		action = menu.exec_(self.mapToGlobal(pos))
		print(action)
	def removeFloatingCards(self):
		self.removeCards(*self.floatingStack.cards)
		self.floatingStack = None
	def grabFloatingCards(self):
		drag = QtGui.QDrag(self)
		mime = QtCore.QMimeData()
		stream = QtCore.QByteArray()
		stream.append(pickle.dumps(tuple(card.d for card in self.floatingStack.cards)))
		mime.setData('cards', stream)
		drag.setMimeData(mime)
		drag.exec_()
	def mousePressEvent(self, event):
		pos = (event.pos().x(), event.pos().y())
		card = self.getTopCollision(pos)
		if card:
			if not card in self.selected: self.updateSelected(card)
			self.resolveEvent(PickupCards, cards=self.selected, pos=pos)
		else:
			self.selectionbox = SelectionBox(self, pos)
		self.redraw()
	def mouseMoveEvent(self, event):
		pos = (event.pos().x(), event.pos().y())
		if self.selectionbox:
			self.selectionbox.resizeTo(pos)
		elif self.selected:
			if pos[0]<0 or pos[1]<0 or self.getSize()[0]<pos[0] or self.getSize()[1]<pos[1]:
				self.grabFloatingCards()
			else:
				for card in self.selected: card.moveTo(*pos)
		self.redraw()
	def mouseReleaseEvent(self, event):
		pos = (event.pos().x(), event.pos().y())
		if self.selectionbox:
			self.selectionbox.end()
			self.selectionbox = None
		if self.floatingStack:
			self.resolveEvent(DropCards, cards=self.selected, pos=pos)
		self.redraw()
	def dragEnterEvent(self, event):
		if event.mimeData().data('cards'): event.accept()
	def dropEvent(self, event):
		if event.source(): event.source().removeFloatingCards()
		pos = (event.pos().x(), event.pos().y())
		self.addCards(*pickle.loads(event.mimeData().data('cards')), pos=pos)
		self.redraw()
	def getSize(self):
		return (self.size().width(), self.size().height())
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
		self.selected.clear()
		self.selected.update(cards)
	def getTopCollision(self, point):
		for i in range(len(self.cards)-1, -1, -1):
			if self.cards[i].rekt.collidepoint(point): return self.cards[i]
		return None
	def getSurface(self):
		self.makeStacks()
		sz = (self.size().width(), self.size().height())
		surface = Surface(sz)
		surface.fill((128, 128, 128))
		for card in self.cards: card.draw(surface)
		for uie in self.uielements: uie.draw(surface)
		return surface
	def addCards(self, *cards, pos = (0, 0)):
		cards = list(DECard(self, card) for card in cards)
		self.cards.extend(cards)
		self.resolveEvent(DropCards, cards=cards, pos=pos)
	def removeCards(self, *cards):
		for card in cards:
			if card in self.cards: self.cards.remove(card)
			if card in self.selected: self.selected.remove(card)
		
def test():
	
	session = DeckEditorSession()
	set = MTGSet(CardLoader.getSets()['KLD'])
	booster = set.generateBooster()
	for card in booster: print(Card.view(card, 'N'))
	session.addCards(*booster)
	session.run()
	
if __name__=='__main__': test()