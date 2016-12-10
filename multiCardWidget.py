from pygame import *
import sys
import math as m
import time
from mtgUtility import *
import time
import threading
from loadImgs import *
from loadCards import *
import numpy as np
import copy
import embedableSurface
from PyQt5 import QtWidgets, QtGui, QtCore
import pickle
import copy

font.init()

class DEImageLoader(ImageLoader):
	imageNameFont = font.Font(None, 18)
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
		try: self.cards.remove(card)
		except ValueError: return
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
	def __init__(self, session, anchor = (0, 0)):
		super(SelectionBox, self).__init__(session)
		self.anchor = np.array(anchor)
		self.corner = np.array(anchor)
		self.pos = [0, 0]
		self.dim = [0, 0]
		self.s = None
		self.newSurface()
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
	def resizeTo(self, pos):
		self.corner = np.array(pos)
		self.newSurface()
		self.updateCollisions()
	def resize(self, rel):
		self.corner += rel
		self.newSurface()
		self.updateCollisions()
	def draw(self, surface):
		surface.blit(self.s, self.pos)
	def updateCollisions(self):
		colrek = Rect(self.pos, self.dim)
		self.session.updateSelected(*tuple(card for card in self.session.cards if card.rekt.colliderect(colrek)))
	def end(self):
		self.updateCollisions()
		self.session.uielements.remove(self)

class FuncWithArg(object):
	def __init__(self, f, *args, **kwargs):
		self.f = f
		self.args = args
		self.kwargs = kwargs
	def run(self):
		self.f(*self.args, **self.kwargs)

class MultiCardWidget(embedableSurface.EmbeddedSurface):
	font = font.Font(None, 30)
	def __init__(self, parent, **kwargs):
		super(MultiCardWidget, self).__init__()
		self.parent = parent
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
		self.setMouseTracking(True)
	def pickupCards(self, *cards, pos=(0, 0)):
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
	def sortCards(self, f=Card.cmcSortValue, row=True, reverse=False):
		if not self.cards: return
		if self.selected: cards = self.selected
		else: cards = self.cards
		sortedcards = sorted(copy.copy(cards), key = lambda o: f(o.d), reverse=reverse)
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
		mapping = {
			rowsort.addAction('CMC'): FuncWithArg(self.sortCards, Card.cmcSortValue),
			rowsort.addAction('Color'): FuncWithArg(self.sortCards, Card.colorSortValue),
			rowsort.addAction('Rarity'): FuncWithArg(self.sortCards, Card.raritySortValue),
			rowsort.addAction('Type'): FuncWithArg(self.sortCards, Card.typeSortValue),
			rowsort.addAction('Is creature'): FuncWithArg(self.sortCards, Card.isCreature, True, True),
			rowsort.addAction('Is permanent'): FuncWithArg(self.sortCards, Card.isPermanent),
			columnsort.addAction('Is creature'): FuncWithArg(self.sortCards, Card.isCreature, False, True),
			columnsort.addAction('Is permanent'): FuncWithArg(self.sortCards, Card.isPermanent, False),
			columnsort.addAction('CMC'): FuncWithArg(self.sortCards, Card.cmcSortValue, False),
			columnsort.addAction('Color'): FuncWithArg(self.sortCards, Card.colorSortValue, False),
			columnsort.addAction('Rarity'): FuncWithArg(self.sortCards, Card.raritySortValue, False),
			columnsort.addAction('Type'): FuncWithArg(self.sortCards, Card.typeSortValue, False)
		}
		menu.addMenu(rowsort)
		menu.addMenu(columnsort)
		action = menu.exec_(self.mapToGlobal(pos))
		if action: mapping[action].run()
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
	def keyPressEvent(self, event):
		key = event.key()
		if key==QtCore.Qt.Key_Delete: self.removeCards(*self.selected)
	def mousePressEvent(self, event):
		if not event.buttons()==QtCore.Qt.LeftButton: return
		self.setFocus(QtCore.Qt.TabFocusReason)
		pos = (event.pos().x(), event.pos().y())
		card = self.getTopCollision(pos)
		if card:
			self.parent.cardadder.setStagingCard(card.d, False)
			if not card in self.selected: self.updateSelected(card)
			self.pickupCards(*self.selected, pos=pos)
		else: self.selectionbox = SelectionBox(self, pos)
		self.redraw()
	def mouseMoveEvent(self, event):
		pos = (event.pos().x(), event.pos().y())
		card = self.getTopCollision(pos)
		if card: self.parent.hover.setCard(card.d)
		if not event.buttons()==QtCore.Qt.LeftButton: return
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
		# if self.stacks:
			# for r in range(len(self.stacks)):
				# for c in range(len(self.stacks[r])):
					# draw.rect(surface, (0, 0, 0), self.stacks[r][c].rekt, 1)
		amountCardTextSurface = self.font.render(str(len(self.cards))+'('+str(len(self.selected))+') cards', 1, (255, 255, 255), (0, 0, 0))
		rekt = amountCardTextSurface.get_rect()
		rekt.move_ip(0, sz[1]-rekt.h)
		surface.blit(amountCardTextSurface, rekt)
		return surface
	def addCards(self, *cards, pos = (0, 0)):
		cards = list(DECard(self, card) for card in cards)
		self.cards.extend(cards)
		self.dropCards(pos, *cards)
		self.redraw()
	def removeCards(self, *cards):
		self.pickupCards(*cards)
		for card in cards:
			try: self.cards.remove(card)
			except ValueError: pass
			try: self.selected.remove(card)
			except KeyError: pass
		self.redraw()
	def clear(self):
		self.pickupCards(*self.cards)
		self.removeFloatingCards()
		self.selected = set()

def test():
	pass
	
if __name__=='__main__': test()