from PyQt5 import QtWidgets, QtGui

class EmbeddedSurface(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(EmbeddedSurface, self).__init__(parent)
		self.setMinimumSize(1, 1)
		self.data = None
		self.image = None
		# if surface: self.updateImage(surface)
	def updateImage(self, surface):
		self.data = surface.get_buffer().raw
		self.image = QtGui.QImage(self.data, surface.get_width(), surface.get_height(), QtGui.QImage.Format_RGB32)
	def getSurface(self):
		raise NotImplemented
	def resizeEvent(self, event):
		self.updateImage(self.getSurface())
	def paintEvent(self, event):
		qp=QtGui.QPainter()
		qp.begin(self)
		qp.drawImage(0, 0, self.image)
		qp.end()
	def redraw(self):
		self.updateImage(self.getSurface())
		self.update()

class MainView(QtWidgets.QWidget):
	def __init__(self,surface,parent=None):
		super(MainView,self).__init__(parent)
		hbox = QtWidgets.QHBoxLayout()
		
		hbox.addWidget(QtWidgets.QPushButton('cool'))
		hbox.addWidget(ImageWidget(surface))
		#hbox.addStretch(1)
		hbox.addWidget(QtWidgets.QPushButton('cool'))
		print('setting layout')
		self.setLayout(hbox)
		
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self,surface,parent=None):
		super(MainWindow,self).__init__(parent)
		self.setCentralWidget(MainView(surface))
		self.setWindowTitle('Simple drag & drop')
		self.setGeometry(300, 300, 300, 200)
		
def test():
	import sys
	app=QtWidgets.QApplication(sys.argv)
	w=MainWindow(s)
	w.show()
	app.exec_()
	
if __name__=='__main__': test()