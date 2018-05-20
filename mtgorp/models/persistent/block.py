import typing as t

from lazy_property import LazyProperty

from orp.database import Model, PrimaryKey
from orp.relationships import Many

from mtgorp.models.interfaces import Expansion
from mtgorp.models.interfaces import Block as _Block


class Block(Model, _Block):
	primary_key = PrimaryKey('name')
	
	def __init__(
		self,
		name,
	):
		self._expansions = Many(self, '_block') #type: Many[Expansion]
	
	@property
	def name(self) -> str:
		return self._name

	@property
	def expansions(self) -> Many[Expansion]:
		return self._expansions

	@LazyProperty
	def expansions_chronologically(self) -> t.List[Expansion]:
		return sorted(self.expansions, key=lambda expansion: expansion.release_date)