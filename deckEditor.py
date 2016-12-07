from multiCardWidget import *

class MainView(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MainView, self).__init__(parent)
		
		set = MTGSet(CardLoader.getCustomSet('BUR'))
		
		main = MultiCardWidget()
		side = MultiCardWidget()
		pool = MultiCardWidget()
		booster = set.generateBooster()
		main.addCards(*booster)
		booster = set.generateBooster()
		side.addCards(*booster)
		booster = set.generateBooster()
		pool.addCards(*booster)
		
		hbox = QtWidgets.QHBoxLayout(self)

		# topleft = QtWidgets.QFrame(self)
		# topleft.setFrameShape(QFrame.StyledPanel)
 
		# topright = QtWidgets.QFrame(self)
		# topright.setFrameShape(QFrame.StyledPanel)

		botsplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
		botsplitter.addWidget(main)
		botsplitter.addWidget(side)

		topsplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		topsplitter.addWidget(pool)
		topsplitter.addWidget(botsplitter)
		
		hbox.addWidget(topsplitter)
		self.setLayout(hbox)
		
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow,self).__init__(parent)
		self.imageloader = DEImageLoader()
		self.setCentralWidget(MainView())
		self.setWindowTitle('Simple drag & drop')
		self.setGeometry(300, 300, 300, 200)
		
def test():
	app=QtWidgets.QApplication(sys.argv)
	
	w=MainWindow()
	w.show()
	app.exec_()
	
if __name__=='__main__': test()