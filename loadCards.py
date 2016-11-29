import json

class CardLoader:
	cards = None
	basecards = None
	cardslist = None
	cardsnamelist = None
	sets = None
	basesets = None
	@staticmethod
	def loadCards():
		CardLoader.cards = json.load(open('cardsFixed.json', encoding='UTF-8'))	
	@staticmethod
	def loadBaseCards():
		CardLoader.basecards = json.load(open('allCards.json', 'r', encoding='UTF-8'))
	@staticmethod
	def loadCardsList():
		CardLoader.cardslist = [CardLoader.getCards()[key] for key in CardLoader.getCards()]
	@staticmethod
	def loadCardsNameList():
		CardLoader.cardsnamelist = list(CardLoader.getCards())
	@staticmethod
	def loadSets():
		CardLoader.sets = json.load(open('setsFixed.json', encoding='UTF-8'))
	@staticmethod
	def loadBaseSets():
		CardLoader.basesets = json.load(open('allSets.json', encoding='UTF-8'))
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
			
		
class CardWriter:
	@staticmethod
	def dump(content, name):
		json.dump(content, open(name, 'w', encoding='UTF-8'))