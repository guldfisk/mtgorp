from models.mtgObjects import *
#
# class PackCard(Card):
# 	def __init__(self, *args, **kwargs):
# 		super(PackCard, self).__init__(*args, **kwargs)
# 		self.content = kwargs.get('content', [])
#
# class OrCard(Card):
# 	def __init__(self, *args, **kwargs):
# 		super(OrCard, self).__init__(*args, **kwargs)
# 		self.options = kwargs.get('options', [])
# 		if not 'name' in self:
# 			self['name'] = self.options[0]['name']+' OR '+self.options[1]['name']
# 		if not 'types' in self:
# 			self['types'] = 'OR card'
# 	def unpack(self):
# 		names = [card['name'] for card in self.options]
# 		name, ok = QtWidgets.QInputDialog.getItem(self.session, 'Select card', 'Select card', names)
# 		if not name or not ok: return
# 		self.session.removeCards(self)
# 		self.session.addCards(self.options[names.index(name)], pos=self.pos)
# 		self.session.redraw()
# 	def rightClicked(self, menu, mapping):
# 		mapping[menu.addAction('Select card')] = FuncWithArg(self.unpack)
		
class CubeBoosterMap(BoosterMap):
	def __init__(self, *args, mset = None, key = None):
		super(CubeBoosterMap, self).__init__(*args, mset=mset, key=key)
		self.shuffle()
	def shuffle(self):
		for slot in self:
			if isinstance(slot, Selector):
				for pair in slot: random.shuffle(pair[1])
			else: random.shuffle(slot)
	def generate_booster(self):
		return Booster([
			option.pop() for option in (
				slot.select()
				if isinstance(slot, Selector) else
				slot
				for slot in self
			)
			if option
		])