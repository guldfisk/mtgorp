import os
import threading

import requests as r

from models import mtgObjects
from resourceload import locate

path = os.path.join(locate.path, 'images')

def get_gatherer_path(s):
	return 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(s)+'&type=card'

class ImageFetcher(threading.Thread):
	def __init__(self, card, parent):
		super(ImageFetcher, self).__init__()
		self.card = card
		self.parent = parent
	def run(self):
		self.parent.fetching.append(self.card['multiverseid'])
		directory_path = self.parent.get_set_path(self.card)
		if not os.path.exists(directory_path):
			os.makedirs(directory_path)
		ro = r.get(get_gatherer_path(self.card['multiverseid']), stream=True)
		with open(self.parent.get_card_path(self.card, 'temp'), 'wb') as f:
			for chunk in ro.iter_content(1024):
				f.write(chunk)
		os.rename(self.parent.get_card_path(self.card, 'temp'), self.parent.get_card_path(self.card, 'jpg'))
		self.parent.fetching.remove(self.card['multiverseid'])

class ImageLoader(object):
	defaultImage = os.path.join(locate.path, 'cardBack.jpg')
	images = {}
	fetching = []
	@staticmethod
	def get_set_key(key):
		if key=='CON':
			return 'CON_'
		else:
			return key
	@staticmethod
	def get_set_path(card):
		return os.path.join(path, ImageLoader.get_set_key(card.get('set', 'NOSET')), '')
	@staticmethod
	def get_card_path(card, extension ='jpg'):
		return os.path.join(
			path,
			ImageLoader.get_set_key(card.get('set', 'NOSET')),
			card['name'].replace('"', '') + '.' + extension
		)
	@staticmethod
	def get_card_identifier(card):
		return mtgObjects.Card.full_name(card).replace('"', '')
	def download_image(self, card):
		if not 'multiverseid' in card or card['multiverseid'] in self.fetching:
			return
		ImageFetcher(card, self).start()
	def load_image(self, card):
		path = self.get_image_path(card)
		if path==self.defaultImage:
			name = 'cardBack'
		else:
			name = ImageLoader.get_card_identifier(card)
		self._load_image(path, name, card)
		return name
	def _load_image(self, path, name, card):
		with open(path, 'rb') as f:
			self.images[name] = f.read()
	def get_default(self):
		if not 'cardBack' in self.images:
			self._load_image(self.defaultImage, 'cardBack', mtgObjects.Card())
		return self.images['cardBack']
	def get_image(self, card):
		if not ImageLoader.get_card_identifier(card) in self.images:
			return self.images[self.load_image(card)]
		return self.images[ImageLoader.get_card_identifier(card)]
	def get_image_path(self, card):
		if not os.path.exists(ImageLoader.get_card_path(card)):
			self.download_image(card)
			return self.defaultImage
		return ImageLoader.get_card_path(card)