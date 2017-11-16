import typing as t

from mtgorp.models.persistent import printing as _printing
from orp import relationships as _relationships
from orp.database import Model, PrimaryKey

class Artist(Model):
	primary_key = PrimaryKey('name')
	def __init__(self, name: str):
		self._faces = _relationships.Many(self, '_artist')
	@property
	def name(self) -> str:
		return self._name
	@property
	def printings(self) -> 't.Tuple[_printing.Printing, ...]':
		return tuple(face.owner for face in self._faces)
