from orp.database import Model, PrimaryKey
from orp.relationships import Many

from lazy_property import LazyProperty

class Block(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name,
	):
		self.expansions = Many(self, '_block')
	@property
	def name(self):
		return self._name
	@LazyProperty
	def expansions_chronologically(self):
		return sorted(self.expansions, key=lambda expansion: expansion.release_date)