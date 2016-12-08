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
import copy

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
	def pickup(self, card):
		if card in self.cards:
			self.take(card)
			return True
	def drop(self, card, pos):
		if self.rekt.collidepoint(pos):
			self.put(card)
			return True
			
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
			
class MultiCardWidget(embedableSurface.EmbeddedSurface, EventSession):
	def __init__(self, **kwargs):
		super(MultiCardWidget, self).__init__(**kwargs)
		self.imageLoader = kwargs.get('imageloader', DEImageLoader())
		self.cards = []
		self.stacks = []
		self.floatingStack = Stack(self)
		self.selectionbox = None
		self.selected = set()
		self.uielements = []
		self.selectionbox = None
		self.lastGridDimensions = (0, 0)
		self.makeStacks()
		self.setAcceptDrops(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.contextMenu)
	def pickupCards(self, pos, *cards):
		self.floatingStack = Stack(self, pos=pos)
		for card in cards: self.pickupCard(card)
	def pickupCard(self, card):
		self.moveCardsToFront(card)
		self.floatingStack.put(card)
		for r in self.stacks:
			for c in r:
				if c.pickup(card): return
	def dropCards(self, pos, *cards):
		for card in cards: self.dropCard(card, pos)
	def dropCard(self, card, pos):
		if card in self.floatingStack.cards: self.floatingStack.cards.remove(card)
		for r in self.stacks:
			for c in r:
				if c.drop(card, pos): return
		card.moveTo(*pos)
	def repositionCard(self, card, pos):
		self.pickupCard(card)
		self.dropCard(card, pos)
	def sortCards(self, f=Card.cmcSortValue, row=True):
		sortedcards = sorted(copy.copy(self.cards), key = lambda o: f(o.d))
		value = f(sortedcards[0].d)
		stack = 0
		for card in sortedcards:
			if not f(card.d)==value:
				stack += 1
				if row and stack>len(self.stacks)-1: stack = len(self.stacks)-1
				elif not row and stack>len(self.stacks[0])-1: stack = len(self.stacks[0])-1
				value = f(card.d)
			if row: self.repositionCard(card, (self.stacks[stack][0].rekt.x, card.rekt.y))
			else: self.repositionCard(card, (card.rekt.x, self.stacks[0][stack].rekt.y))
		self.redraw()
	def contextMenu(self, pos):
		menu = QtWidgets.QMenu()
		rowsort = QtWidgets.QMenu('Sort rows')
		columnsort = QtWidgets.QMenu('Sort columns')
		rowcmc = rowsort.addAction('CMC')
		rowcolor = rowsort.addAction('Color')
		rowrarity = rowsort.addAction('Rarity')
		rowispermanent = rowsort.addAction('Is permanent')
		columncmc = columnsort.addAction('CMC')
		columncolor = columnsort.addAction('Color')
		columnrarity = columnsort.addAction('Rarity')
		columnispermanent = columnsort.addAction('Is permanent')
		menu.addMenu(rowsort)
		menu.addMenu(columnsort)
		action = menu.exec_(self.mapToGlobal(pos))
		if action==rowcmc: self.sortCards(Card.cmcSortValue)
		elif action==rowcolor: self.sortCards(Card.colorSortValue)
		elif action==rowrarity: self.sortCards(Card.raritySortValue)
		elif action==rowispermanent: self.sortCards(Card.isPermanent)
		elif action==columncmc: self.sortCards(Card.cmcSortValue, False)
		elif action==columncolor: self.sortCards(Card.colorSortValue, False)
		elif action==columnrarity: self.sortCards(Card.raritySortValue, False)
		elif action==columnispermanent: self.sortCards(Card.isPermanent, False)
	def removeFloatingCards(self):
		self.removeCards(*self.floatingStack.cards)
		self.floatingStack.cards[:] = []
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
			self.pickupCards(pos, *self.selected)
		else: self.selectionbox = SelectionBox(self, pos)
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
		if self.floatingStack.cards:
			self.dropCards(pos, *self.floatingStack.cards)
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
		x, y = self.getSize()
		if (x, y)==self.lastGridDimensions: return
		self.lastGridDimensions = (x, y)
		self.stacks[:] = []
		w, h = self.imageLoader.getDefault().get_rect().w, self.imageLoader.getDefault().get_rect().h
		rows, columns = max(m.floor(x/w), 1), min(max(m.floor(y/h), 1), 2)
		for r in range(rows):
			self.stacks.append([])
			for c in range(columns):
				stack = Stack(self)
				stack.resize(int(x/rows*r), int(y/columns*c), int(x/rows), int(y/columns))
				self.stacks[r].append(stack)
		for card in self.cards: self.dropCard(card, (card.rekt.centerx, card.rekt.centery))
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
		if self.stacks:
			for r in range(len(self.stacks)):
				for c in range(len(self.stacks[r])):
					draw.rect(surface, (0, 0, 0), self.stacks[r][c].rekt, 1)
		return surface
	def addCards(self, *cards, pos = (0, 0)):
		cards = list(DECard(self, card) for card in cards)
		self.cards.extend(cards)
		self.dropCards(pos, *cards)
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