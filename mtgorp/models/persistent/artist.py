import typing as t

from orp import relationships as _relationships
from orp.models import Model, PrimaryKey

from mtgorp.models.interfaces import Artist as _Artist
from mtgorp.models.interfaces import Face


class Artist(Model, _Artist):
    primary_key = PrimaryKey("name")
    _name: str

    def __init__(self, name: str):
        self._faces = _relationships.Many(self, "_artist")

    @property
    def faces(self) -> t.AbstractSet[Face]:
        return self._faces

    @property
    def name(self) -> str:
        return self._name
