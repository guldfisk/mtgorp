import copy

from resourceload import cardload

#Gets printings and flavors for a card
def _get_printings(card_name, sets):
	printings = []
	flavors = {}
	for key in sets:
		for card in sets[key]['cards']:
			if card['name']==card_name:
				printings.append(key)
				flavors[key] = card.get('flavor', '')
	return printings, flavors

#Adds printings and flavors to allCards.json
def make_cards_fixed():
	cards = copy.deepcopy(cardload.CardLoader.get_base_cards())
	sets = cardload.CardLoader.get_base_sets()
	for name in cards:
		cards[name]['printings'], cards[name]['flavors'] = _get_printings(name, sets)
		if 'names' in cards[name]:
			cards[name]['isFront'] = name==cards[name]['names'][0]
	cardload.CardWriter.dump(cards, 'cardsFixed.json')

def make_sets_fixed():
	sets = copy.deepcopy(cardload.CardLoader.get_base_sets())
	for key in sets:
		for card in sets[key]['cards']:
			if 'names' in card: card['isFront'] = card['name']==card['names'][0]
			card['set'] = key
	cardload.CardWriter.dump(sets, 'SetsFixed.json')