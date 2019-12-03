import typing as t

from orp import relationships as _relationships
from orp.database import Model, PrimaryKey

from mtgorp.models.interfaces import Printing
from mtgorp.models.interfaces import Artist as _Artist


class Artist(Model, _Artist):
    primary_key = PrimaryKey('name')
    _name: str

    def __init__(self, name: str):
        self._faces = _relationships.Many(self, '_artist')

    @property
    def name(self) -> str:
        return self._name

    @property
    def printings(self) -> t.Tuple[Printing, ...]:
        return tuple(face.owner for face in self._faces)
