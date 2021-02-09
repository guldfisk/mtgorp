from __future__ import annotations

import typing as t

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.interfaces import Printing
from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator


class Deck(Serializeable):

    def __init__(
        self,
        maindeck: t.Union[t.Iterable[Printing], t.Iterable[t.Tuple[Printing, int]]],
        sideboard: t.Union[t.Iterable[Printing], t.Iterable[t.Tuple[Printing, int]], None] = None,
    ):
        self._maindeck: FrozenMultiset[Printing] = (
            maindeck
            if isinstance(maindeck, FrozenMultiset)
            else FrozenMultiset(maindeck)
        )

        self._sideboard: FrozenMultiset[Printing] = (
            (
                sideboard
                if isinstance(sideboard, FrozenMultiset) else
                FrozenMultiset(sideboard)
            )
            if sideboard is not None else
            FrozenMultiset()
        )

    @property
    def maindeck(self) -> FrozenMultiset[Printing]:
        return self._maindeck

    @property
    def sideboard(self) -> FrozenMultiset[Printing]:
        return self._sideboard

    @property
    def seventy_five(self) -> FrozenMultiset[Printing]:
        return self._maindeck + self._sideboard

    def __iter__(self) -> t.Iterable[Printing]:
        return self.seventy_five.__iter__()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Deck)
            and self._maindeck == other.maindeck
            and self._sideboard == other.sideboard
        )

    def __hash__(self) -> int:
        return hash(self.seventy_five)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({len(self._maindeck)}, {len(self._sideboard)})'

    def serialize(self) -> serialization_model:
        return {
            'maindeck': list(self._maindeck),
            'sideboard': list(self._sideboard),
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> Deck:
        return Deck(
            inflator.inflate_all(Printing, value['maindeck']),
            inflator.inflate_all(Printing, value.get('sideboard', ())),
        )
