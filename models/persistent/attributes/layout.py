from abc import ABCMeta

from orp.relationships import OneToOne, OneDescriptor, ManyToOne, OneToMany, Group, Relationship

class LayoutRelationship(Relationship):
	@property
	def owner(self):
		return self._owner.owner
	@staticmethod
	def from_owner(owner):
		return owner.layout

class LayoutCardGroup(Group, LayoutRelationship):
	pass

class CardToLayout(OneToOne, LayoutRelationship):
	pass

class CardToLayouts(OneToMany, LayoutRelationship):
	pass

class CardsToLayout(ManyToOne, LayoutRelationship):
	pass

class Layout(object):
	def __init__(self, owner, layout_type: str):
		self.owner = owner
		self._layout_type = layout_type
	@property
	def layout_type(self):
		return self._layout_type
	def __eq__(self, other):
		return isinstance(other, Layout) and self._layout_type == other.layout_type
	def __hash__(self):
		return hash(self._layout_type)
	def __str__(self):
		return self._layout_type

class Standard(Layout):
	def __init__(self, owner):
		super().__init__(owner, 'standard')

class TwoSided(Layout, metaclass=ABCMeta):
	def __init__(self, owner, is_front=True):
		super().__init__(owner, 'transform')
		self._other_side = CardToLayout(self, '_other_side')
		self._is_front = is_front
	other_side = OneDescriptor('_other_side')
	@property
	def is_front(self):
		return self._is_front

class Transform(TwoSided):
	pass

class Flip(TwoSided):
	pass

class Split(Layout):
	def __init__(self, owner):
		super().__init__(owner, 'split')
		self.other_cards = LayoutCardGroup(self, 'other_cards')

class Meld(Layout, metaclass=ABCMeta):
	def __init__(self, owner, is_front=True):
		super().__init__(owner, 'meld')
		self._is_front = is_front
	@property
	def is_front(self):
		return self._is_front

class MeldFront(Meld):
	def __init__(self, owner):
		super().__init__(owner)
		self._back_side = CardToLayouts(self, 'front_sides')
	back_side = OneDescriptor('_back_side')

class MeldBack(Meld):
	def __init__(self, owner):
		super().__init__(owner, is_front=False)
		self.front_sides = CardsToLayout(self, '_back_side')