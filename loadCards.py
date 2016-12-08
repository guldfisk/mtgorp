import json
import os

class CardLoader:
	cards = None
	basecards = None
	cardslist = None
	cardsnamelist = None
	sets = None
	basesets = None
	customSets = dict()
	@staticmethod
	def loadCards(path=''):
		CardLoader.cards = json.load(open(os.path.join(path, 'cardsFixed.json'), encoding='UTF-8'))	
	@staticmethod
	def loadBaseCards(path=''):
		CardLoader.basecards = json.load(open(os.path.join(path, 'allCards.json'), 'r', encoding='UTF-8'))
	@staticmethod
	def loadCardsList():
		CardLoader.cardslist = [CardLoader.getCards()[key] for key in CardLoader.getCards()]
	@staticmethod
	def loadCardsNameList():
		CardLoader.cardsnamelist = list(CardLoader.getCards())
	@staticmethod
	def loadSets(path=''):
		CardLoader.sets = json.load(open(os.path.join(path, 'setsFixed.json'), encoding='UTF-8'))
	@staticmethod
	def loadBaseSets(path=''):
		CardLoader.basesets = json.load(open(os.path.join(path, 'allSets.json'), encoding='UTF-8'))
	@staticmethod
	def loadCustomSet(name, path=''):
		if not os.path.exists(os.path.join(path, 'customSets', name+'.json')): return
		CardLoader.customSets[name] = json.load(open(os.path.join(path, 'customSets', name+'.json'), encoding='UTF-8'))
		return True
	@staticmethod
	def getCards():
		if CardLoader.cards==None: CardLoader.loadCards()
		return CardLoader.cards
	@staticmethod
	def getBaseCards():
		if CardLoader.basecards==None: CardLoader.loadBaseCards()
		return CardLoader.basecards
	@staticmethod
	def getCardsList():
		if CardLoader.cardslist==None: CardLoader.loadCardsList()
		return CardLoader.cardslist
	@staticmethod
	def getCardsNameList():
		if CardLoader.cardsnamelist==None: CardLoader.loadCardsNameList()
		return CardLoader.cardsnamelist
	@staticmethod
	def getSets():
		if CardLoader.sets==None: CardLoader.loadSets()
		return CardLoader.sets
	@staticmethod
	def getBaseSets():
		if CardLoader.basesets==None: CardLoader.loadBaseSets()
		return CardLoader.basesets
	def getCustomSet(name):
		if not name in CardLoader.customSets:
			if not CardLoader.loadCustomSet(name): return
		return CardLoader.customSets[name]
			
class CardWriter:
	@staticmethod
	def dump(content, name):
		json.dump(content, open(name, 'w', encoding='UTF-8'))