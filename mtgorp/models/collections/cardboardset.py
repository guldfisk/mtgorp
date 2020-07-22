from __future__ import annotations

import typing as t

from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator


class CardboardSet(Serializeable):

    def __init__(self, cardboards: t.Optional[t.Iterable[Cardboard]] = None):
        self._cardboards = frozenset() if cardboards is None else frozenset(cardboards)

    @property
    def cardboards(self) -> t.AbstractSet[Cardboard]:
        return self._cardboards
    
    def serialize(self) -> serialization_model:
        return {
            'cardboards': list(self._cardboards),
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> CardboardSet:
        return cls(inflator.inflate_all(Cardboard, value['cardboards']))

    def __hash__(self) -> int:
        return self._cardboards.__hash__()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._cardboards == other._cardboards
        )

    def __iter__(self) -> t.Iterator[Cardboard]:
        return self._cardboards.__iter__()

    def __or__(self, other: CardboardSet) -> CardboardSet:
        return self.__class__(self._cardboards | other._cardboards)

    def __sub__(self, other: CardboardSet) -> CardboardSet:
        return self.__class__(self._cardboards - other._cardboards)

    def __repr__(self) -> str:
        return self._cardboards.__repr__()
