from orp.relationships import Many
from orp.database import Model, PrimaryKey

class Artist(Model):
	primary_key = PrimaryKey('name')
	def __init__(self, name: str):
		self.name = name
		self._faces = Many(self, '_artist')
	@property
	def printings(self):
		return tuple(face.owner for face in self._faces)
