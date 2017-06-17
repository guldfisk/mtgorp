import json
import os
import threading

from managejson import update
from resourceload.locate import Locator

path = os.path.join(Locator.path, 'jsons')

class _JsonFetcher(threading.Thread):
	def __init__(self, parent):
		super(_JsonFetcher, self).__init__()
		self.parent = parent
	def run(self):
		print('start fetch thread')
		self.parent._fetching.append(self)
		val = update.check_and_update()
		print(val)
		if val:
			self.parent.init()
		self.parent._fetching.remove(self)
		print('finish fetch thread')

class CardLoader:
	_fetching = []
	@staticmethod
	def init():
		CardLoader.cards = None
		CardLoader.base_cards = None
		CardLoader.cards_list = None
		CardLoader.cards_name_list = None
		CardLoader.sets = None
		CardLoader.base_sets = None
		CardLoader.custom_sets = None
	@staticmethod
	def update():
		if not CardLoader._fetching:
			_JsonFetcher(CardLoader).start()
	@staticmethod
	def _load(path, default):
		if os.path.exists(path):
			return json.load(open(path, 'r', encoding='UTF-8'))
		else:
			CardLoader.update()
			return default
	@staticmethod
	def load_cards(path=path):
		print('loading cards')
		CardLoader.cards = CardLoader._load(os.path.join(path, 'cardsFixed.json'), dict())
	@staticmethod
	def load_base_cards(path=path):
		CardLoader.base_cards = CardLoader._load(os.path.join(path, 'allCards.json'), dict())
	@staticmethod
	def load_cards_list():
		CardLoader.cards_list = [CardLoader.get_cards()[key] for key in CardLoader.get_cards()]
	@staticmethod
	def load_cards_name_list():
		CardLoader.cards_name_list = list(CardLoader.get_cards())
	@staticmethod
	def load_sets(path=path):
		CardLoader.sets = CardLoader._load(os.path.join(path, 'setsFixed.json'), dict())
	@staticmethod
	def load_base_sets(path=path):
		CardLoader.base_sets = CardLoader._load(os.path.join(path, 'allSets.json'), dict())
	@staticmethod
	def load_custom_sets(name, path=path):
		if not os.path.exists(os.path.join(path, 'customSets', name+'.json')):
			return
		CardLoader.custom_sets[name] = json.load(open(os.path.join(path, 'customSets', name+'.json'), encoding='UTF-8'))
		return True
	@staticmethod
	def get_cards():
		if CardLoader.cards is None:
			CardLoader.load_cards()
		return CardLoader.cards
	@staticmethod
	def get_base_cards():
		if CardLoader.base_cards is None:
			CardLoader.load_base_cards()
		return CardLoader.base_cards
	@staticmethod
	def get_cards_list():
		if CardLoader.cards_list is None:
			CardLoader.load_cards_list()
		return CardLoader.cards_list
	@staticmethod
	def get_cards_name_list():
		if CardLoader.cards_name_list is None:
			CardLoader.load_cards_name_list()
		return CardLoader.cards_name_list
	@staticmethod
	def get_sets():
		if CardLoader.sets is None:
			CardLoader.load_sets()
		return CardLoader.sets
	@staticmethod
	def get_base_sets():
		if CardLoader.base_sets is None:
			CardLoader.load_base_sets()
		return CardLoader.base_sets
	@staticmethod
	def get_custom_set(name):
		if not name in CardLoader.customSets:
			if not CardLoader.load_custom_sets(name):
				return
		return CardLoader.customSets[name]

CardLoader.init()

class CardWriter:
	@staticmethod
	def dump_to(content, dest_path=path):
		json.dump(content, open(dest_path, 'w', encoding='UTF-8'))
	@staticmethod
	def dump(content, dest_path):
		CardWriter.dump_to(content, os.path.join(path, dest_path))