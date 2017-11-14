import typing as t

from mtgorp.models.persistent import expansion as _expansion
from orp.database import Model, PrimaryKey
from orp.relationships import Many

from lazy_property import LazyProperty

class Block(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name,
	):
		self.expansions = Many(self, '_block') #type: t.Set[_expansion.Expansion]
	@property
	def name(self) -> str:
		return self._name
	@LazyProperty
	def expansions_chronologically(self) -> 't.List[_expansion.Expansion]':
		return sorted(self.expansions, key=lambda expansion: expansion.release_date)