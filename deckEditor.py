from multiCardWidget import *
import cardSearch

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
			self.setCurrentRow(0)
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
	def setStagingCard(self, card):
		self.stagingCard = card
		self.currentadding.setText(Card.view(card, 'N'))
		self.amountedit.setFocus(QtCore.Qt.TabFocusReason)
	
class HoverWidget(embedableSurface.EmbeddedSurface):
	def __init__(self, parent):
		super(HoverWidget, self).__init__()
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
			
		booster = set.generateBooster()
		self.cardWidgets['side'].addCards(*booster)
		booster = set.generateBooster()
		self.cardWidgets['pool'].addCards(*booster)
		
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
		self.setCentralWidget(MainView())
		
		self.setWindowTitle('Deckeditor')
		exitAction = QtWidgets.QAction('&Exit', self)		
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtWidgets.qApp.quit)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		
		self.setGeometry(300, 300, 300, 200)
		
def test():
	app=QtWidgets.QApplication(sys.argv)
	
	w=MainWindow()
	w.show()
	sys.exit(app.exec_())
	
if __name__=='__main__': test()