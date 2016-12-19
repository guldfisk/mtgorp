import copy
import json

#Adds printings and flavors to allCards.json
def makeCardsFixed():
	cards = copy.deepcopy(CardLoader.getBaseCards())
	sets = CardLoader.getBaseSets()
	for name in cards:
		cards[name]['printings'], cards[name]['flavors'] = getPrintings(name, sets)
		if 'names' in cards[name]: cards[name]['isFront'] = name==cards[name]['names'][0]
	CardWriter.dump(cards, 'cardsFixed.json')

def makeSetsFixed():
	sets = copy.deepcopy(CardLoader.getBaseSets())
	for key in sets:
		for card in sets[key]['cards']:
			if 'names' in card: card['isFront'] = card['name']==card['names'][0]
			card['set'] = key
	CardWriter.dump(sets, 'SetsFixed.json')

#Gets printings and flavors for a card
def getPrintings(cardName, sets):
	printings = []
	flavors = {}
	for key in sets:
		for card in sets[key]['cards']:
			if card['name']==cardName:
				printings.append(key)
				flavors[key] = card.get('flavor', '')
	return(printings, flavors)