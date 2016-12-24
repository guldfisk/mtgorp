from multiCardWidget import *
import cardSearch
import os

class LineEditWithDropDown(QtWidgets.QLineEdit):
	def __init__(self, parent):
		super(LineEditWithDropDown, self).__init__(parent)
		self.parent = parent
		self.dropdown = QtWidgets.QListWidget()
		self.dropdown.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint+QtCore.Qt.WindowStaysOnTopHint))
		self.dropdown.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
		self.textEdited.connect(self.onTextEdited)
	def setCurrentRow(self, value):
		self.dropdown.setCurrentRow(value)
	def keyPressEvent(self, event):
		key = event.key()
		if key==QtCore.Qt.Key_Down:
			newrow = self.dropdown.currentRow()+1
			if newrow>self.dropdown.count()-1: newrow = self.dropdown.count()-1
			self.setCurrentRow(newrow)
		elif key==QtCore.Qt.Key_Up:
			newrow = self.dropdown.currentRow()-1
			if newrow<0: newrow = 0
			self.setCurrentRow(newrow)
		elif key==QtCore.Qt.Key_Return:
			self.out()
		elif key==QtCore.Qt.Key_Escape:
			self.clear()
		else: super(LineEditWithDropDown, self).keyPressEvent(event)
	def paintEvent(self, event):
		super(LineEditWithDropDown, self).paintEvent(event)
		if not self.text():
			self.dropdown.hide()
			return
		self.dropdown.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))
		if not self.dropdown.isVisible(): self.dropdown.show()
	def onTextEdited(self):
		self.dropdown.clear()
		self.getRows()
		self.setCurrentRow(0)
	def out(self):
		pass
	def getRows(self):
		for i in range(5): self.dropdown.addItem(self.text()+str(i))

class CardAdderLineEditWithDropDown(LineEditWithDropDown):
	def __init__(self, parent):
		super(CardAdderLineEditWithDropDown, self).__init__(parent)
		self.hits = None
		self.cards = cardSearch.CardList(sorted(CardLoader.getCardsList(), key = lambda card: card['name']))
	def setCurrentRow(self, value):
		super(CardAdderLineEditWithDropDown, self).setCurrentRow(value)
		if self.hits: self.parent.parent.hover.setCard(Card.getPrintable(self.hits.peekMultiple(10)[value]))
	def out(self):
		if self.hits:
			self.parent.setStagingCard(Card.getPrintable(self.hits.peekMultiple(10)[self.dropdown.currentRow()]))
			self.clear()
	def getRows(self):
		self.hits = self.cards.matchList(cardSearch.CardMatch(self.text()))
		for peek in self.hits.peekMultiple(10): self.dropdown.addItem(Card.view(peek, 'N'))

class AmountCardAdder(QtWidgets.QLineEdit):
	def __init__(self, parent):
		super(AmountCardAdder, self).__init__(parent)
		self.parent = parent
		self.setValidator(QtGui.QIntValidator(0, 255, self))
	def keyPressEvent(self, event):
		key = event.key()
		if key==QtCore.Qt.Key_Return and self.parent.stagingCard:
			tx = self.text()
			if not tx: amnt = 1
			else: amnt = int(tx)
			for i in range(amnt): self.parent.parent.cardWidgets[self.parent.targetzone.currentText()].addCards(self.parent.stagingCard)
			self.parent.lineedit.setFocus(QtCore.Qt.TabFocusReason)
		else: super(AmountCardAdder, self).keyPressEvent(event)

class CardAdder(QtWidgets.QWidget):
	def __init__(self, parent):
		super(CardAdder, self).__init__()
		self.parent = parent
		self.setMaximumSize(223, 310)
		self.stagingCard = None
		
		box = QtWidgets.QVBoxLayout(self)
		
		self.lineedit = CardAdderLineEditWithDropDown(self)
		self.amountedit = AmountCardAdder(self)
		self.currentadding = QtWidgets.QLabel()
		
		hbox = QtWidgets.QHBoxLayout(self)
		
		hbox.addWidget(self.currentadding)
		hbox.addWidget(self.amountedit)
		
		self.targetzone = QtWidgets.QComboBox()
		
		for item in ('main', 'side', 'pool'): self.targetzone.addItem(item)
		
		box.addWidget(self.lineedit)
		box.addLayout(hbox)
		box.addWidget(self.targetzone)
		box.addStretch(1)
		self.setLayout(box)
	def setStagingCard(self, card, setFocus=True):
		self.stagingCard = card
		self.currentadding.setText(Card.view(card, 'N'))
		if setFocus: self.amountedit.setFocus(QtCore.Qt.TabFocusReason)

class HoverImage(embedableSurface.EmbeddedSurface):
	def __init__(self, parent):
		super(HoverImage, self).__init__(parent)
		self.parent = parent
		self.card = None
		self.setMinimumSize(223, 310)
		self.setMaximumSize(223, 310)
	def getSurface(self):
		surface = Surface((223, 310))
		if not self.card: return surface
		self.parent.imageloader.getImage(self.card)
		card = self.parent.imageloader.images.get(self.card.fullName()+'_full', Surface((0, 0)))
		if card: surface.blit(card, card.get_rect())
		return surface
	def setCard(self, card):
		self.card = card
		self.redraw()

class HoverWidget(QtWidgets.QWidget):
	def __init__(self, parent):
		super(HoverWidget, self).__init__(parent)
		
		self.setMaximumWidth(250)
		
		self.image = HoverImage(parent)
		self.label = QtWidgets.QTextEdit()
		
		self.label.setReadOnly(True)
		
		box = QtWidgets.QVBoxLayout(self)
		
		box.addWidget(self.image)
		box.addWidget(self.label)
		
		self.setLayout(box)
		
	def setCard(self, card):
		if not card: return
		self.image.setCard(card)
		self.label.setText(Card.view(card, 'nmtRXsop'))

class MainView(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MainView, self).__init__(parent)
		self.imageloader = DEImageLoader()
		
		set = MTGSet(CardLoader.getSets()['KLD'])
		
		self.hover = HoverWidget(self)
		self.cardadder = CardAdder(self)
		
		self.cardWidgets = {
			'main': MultiCardWidget(self, imageloader=self.imageloader),
			'side': MultiCardWidget(self, imageloader=self.imageloader),
			'pool': MultiCardWidget(self, imageloader=self.imageloader)
		}
		
		box = QtWidgets.QHBoxLayout(self)

		botsplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		botsplitter.addWidget(self.cardWidgets['main'])
		botsplitter.addWidget(self.cardWidgets['side'])

		topsplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		topsplitter.addWidget(self.cardWidgets['pool'])
		topsplitter.addWidget(botsplitter)
		
		vbox = QtWidgets.QVBoxLayout(self)
		
		vbox.addWidget(self.cardadder)
		vbox.addWidget(self.hover)
		
		box.addWidget(topsplitter)
		box.addLayout(vbox)
		
		self.setLayout(box)

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow,self).__init__(parent)
		self.imageloader = DEImageLoader()
		
		self.setWindowIcon(QtGui.QIcon(os.path.join('resources', 'handelsforbud.png')))
		
		self.mainview = MainView()
		
		self.setCentralWidget(self.mainview)
		
		self.setWindowTitle('Deckeditor')
		
		menubar = self.menuBar()
		
		allMenues = {
			menubar.addMenu('File'): (
				('Exit', 'Ctrl+Q', QtWidgets.qApp.quit),
				('Load Deck', 'Ctrl+O', self.load),
				('Load Pool', 'Ctrl+P', self.loadPool),
				('Save deck', 'Ctrl+S', self.save),
				('Save pool', 'Ctrl+l', self.savePool)
			),
			menubar.addMenu('Generate'): (
				('Sealed pool', 'Ctrl+G', self.generatePool),
				('Cube Pools', 'Ctrl+C', self.generateCubePools)
			),
			menubar.addMenu('Add'): (
				('Add cards', 'Ctrl+f', self.addCard),
			)
		}
	
		for menu in allMenues:
			for subMenu in allMenues[menu]:
				action = QtWidgets.QAction(subMenu[0], self)
				action.setShortcut(subMenu[1])
				action.triggered.connect(subMenu[2])
				menu.addAction(action)
		
		self.setGeometry(300, 300, 300, 200)
	def addCard(self):
		self.mainview.cardadder.lineedit.setFocus(QtCore.Qt.TabFocusReason)
	def savePool(self):
		self.save(True)
	def loadPool(self):
		self.load(True)
	def generateCubePools(self):
		saveDialog = QtWidgets.QFileDialog()
		saveDialog.setFileMode(QtWidgets.QFileDialog.Directory)
		saveDialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
		saveDialog.exec_()
		fname = saveDialog.selectedFiles()
		if not fname or not fname[0]: return
		text, ok = QtWidgets.QInputDialog.getText(self, 'Select set and pack amount', 'Type key:')
		if ok: s = str(text)
		else: return
		cards = []
		m = re.match('(\d*)([^\s\d]+)(\d*)', s)
		if not m: return
		size, setcode, amnt = m.groups()
		if not size: size = 1
		else: size = int(size)
		if not amnt: amnt = 1
		else: amnt = int(amnt)
		if setcode in CardLoader.getSets(): mset = MTGSet(CardLoader.getSets()[setcode])
		elif CardLoader.getCustomSet(setcode): mset = MTGSet(CardLoader.getCustomSet(setcode))
		else: return

		map = mset.generateCubeBoosterMap()

		for i in range(int(amnt)):
			boosters = [map.generateBooster() for n in range(size)]
			pool = Pool(boosters = boosters)
			with open(os.path.join(fname[0], setcode+'_pool_'+str(i)+'.pool'), 'w') as f: f.write(pool.toJson())
	
	def load(self, asPool=False):
		fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Deck', '')
		if not fname or not fname[0]: return
		content = ''
		with open(fname[0], 'r') as f: content = f.read()
		for key in self.mainview.cardWidgets: self.mainview.cardWidgets[key].clear()
		if asPool:
			pool = Pool(s=content)
			self.mainview.cardWidgets['pool'].addCards(*pool)
		else:
			deck = Deck(content)
			self.mainview.cardWidgets['main'].addCards(*deck.maindeck)
			self.mainview.cardWidgets['side'].addCards(*deck.sideboard)
	def save(self, asPool=False):
		fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Deck', '')
		if not fname or not fname[0]: return
		fname = fname[0]
		extension = re.match('.*?\.([^\.]+)', fname, re.DOTALL)
		if not extension:
			if asPool:
				extension = 'pool'
				fname += '.pool'
			else:
				extension = 'dec'
				fname += '.dec'
		else: extension = extension.groups()[0]
		if asPool:
			cards = Pool([card.d for key in self.mainview.cardWidgets for card in self.mainview.cardWidgets[key].cards])
		else:
			cards = Deck(
				maindeck=[card.d for card in self.mainview.cardWidgets['main'].cards],
				sideboard=[card.d for card in self.mainview.cardWidgets['side'].cards]
			)
		if extension in ('xml', 'cod'): content = ET.tostring(cards.toXML().getroot(), 'UTF-8').decode('UTF-8')
		elif extension in ('json', 'pool'): content = cards.toJson()
		else: content = cards.toString()
		with open(fname, 'w') as f: f.write(content)
	def generatePool(self):
		text, ok = QtWidgets.QInputDialog.getText(self, 'Pool generator', 'Type key:')
		if ok: s = str(text)
		else: return
		cards = []
		for m in re.finditer('(\d*)([^\s]+)', s):
			amnt, setcode = m.groups()
			if not amnt: amnt = 1
			if setcode in CardLoader.getSets(): mset = MTGSet(CardLoader.getSets()[setcode])
			elif CardLoader.getCustomSet(setcode): mset = MTGSet(CardLoader.getCustomSet(setcode))
			else: continue
			for i in range(int(amnt)): cards.extend(mset.generateBooster())
		for key in self.mainview.cardWidgets: self.mainview.cardWidgets[key].clear()
		self.mainview.cardWidgets['pool'].addCards(*cards)
		
def test():
	app=QtWidgets.QApplication(sys.argv)
	
	w=MainWindow()
	w.show()
	sys.exit(app.exec_())
	
if __name__=='__main__': test()