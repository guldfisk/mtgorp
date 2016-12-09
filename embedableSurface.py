from PyQt5 import QtWidgets, QtGui

class EmbeddedSurface(QtWidgets.QWidget):
	def __init__(self):
		super(EmbeddedSurface, self).__init__()
		self.setMinimumSize(1, 1)
		self.data = None
		self.image = None
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
