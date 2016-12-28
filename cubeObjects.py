from mtgObjects import *

class PackCard(Card):
	def __init__(self, *args, **kwargs):
		super(PackCard, self).__init__(*args, **kwargs)
		self.content = kwargs.get('content', [])

class CubeBoosterMap(BoosterMap):
	def __init__(self, *args, mset = None, key = None):
		super(CubeBoosterMap, self).__init__(*args, mset=mset, key=key)
		self.shuffle()
	def shuffle(self):
		for slot in self:
			if isinstance(slot, Selector):
				for pair in slot: random.shuffle(pair[1])
			else: random.shuffle(slot)
	def generateBooster(self):
		return Booster([
			option.pop() for option in (
				slot.select()
				if isinstance(slot, Selector) else
				slot
				for slot in self
			)
			if option
		])