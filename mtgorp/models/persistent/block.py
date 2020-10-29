from orp.models import Model, PrimaryKey
from orp.relationships import Many

from mtgorp.models.interfaces import Expansion
from mtgorp.models.interfaces import Block as _Block


class Block(Model, _Block):
    primary_key = PrimaryKey('name')
    _name: str

    def __init__(
        self,
        name,
    ):
        self._expansions: Many[Expansion] = Many(self, '_block')

    @property
    def name(self) -> str:
        return self._name

    @property
    def expansions(self) -> Many[Expansion]:
        return self._expansions
