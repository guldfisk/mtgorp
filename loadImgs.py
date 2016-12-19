import threading
import requests as r
import os
from loadCards import *
from mtgObjects import *

def gathererPath(s):
	return('http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(s)+'&type=card')

class CardFetcher(threading.Thread):
	def __init__(self, card, parent):
		super(CardFetcher, self).__init__()
		self.card = card
		self.parent = parent
	def run(self):
		self.parent.fetching.append(self.card['multiverseid'])
		dirPath = self.parent.getSetPath(self.card)
		if not os.path.exists(dirPath): os.makedirs(dirPath)
		ro = r.get(gathererPath(self.card['multiverseid']), stream=True)
		with open(self.parent.getCardPath(self.card, 'temp'), 'wb') as f:
			for chunk in ro.iter_content(1024): f.write(chunk)
		os.rename(self.parent.getCardPath(self.card, 'temp'), self.parent.getCardPath(self.card, 'jpg'))
		self.parent.fetching.remove(self.card['multiverseid'])

class ImageLoader(object):
	defaultImage = os.path.join('resources', 'cardBack.jpg')
	images = {}
	fetching = []
	@staticmethod
	def getSetKey(key):
		if key=='CON': return 'CON_'
		else: return key
	@staticmethod
	def getSetPath(card):
		return os.path.join('images', ImageLoader.getSetKey(card.get('set', 'NOSET')), '')
	@staticmethod
	def getCardPath(card, extension = 'jpg'):
		return os.path.join('images', ImageLoader.getSetKey(card.get('set', 'NOSET')), card['name']+'.'+extension)
	def downImage(self, card):
		if not 'multiverseid' in card or card['multiverseid'] in self.fetching: return
		CardFetcher(card, self).start()
	def loadImage(self, card):
		path = self.getImagePath(card)
		if path==self.defaultImage: name = 'cardBack'
		else: name = Card.fullName(card)
		self._loadImage(path, name, card)
		return name
	def _loadImage(self, path, name, card):
		with open(path, 'rb') as f: self.images[name] = f.read()
	def getDefault(self):
		if not 'cardBack' in self.images: self._loadImage(self.defaultImage, 'cardBack', Card())
		return self.images['cardBack']
	def getImage(self, card):
		if not Card.fullName(card) in self.images:
			return self.images[self.loadImage(card)]
		return self.images[Card.fullName(card)]
	def getImagePath(self, card):
		if not os.path.exists(ImageLoader.getCardPath(card)):
			self.downImage(card)
			return self.defaultImage
		return ImageLoader.getCardPath(card)
		
def test():
	imageloader = ImageLoader()
	print(imageloader.getImagePath(CardLoader.getSets()['EMN']['cards'][4]))
	
if __name__=='__main__': test()