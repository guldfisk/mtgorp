from __future__ import annotations

import typing as t

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.interfaces import Printing
from mtgorp.models.collections.deck import Deck
from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator


class Pool(Serializeable):

    def __init__(
        self,
        printings: t.Iterable[Printing],
        decks: t.Optional[t.Iterable[Deck]] = None,
    ):
        self._printings: FrozenMultiset[Printing] = (
            printings
            if isinstance(printings, FrozenMultiset) else
            FrozenMultiset(printings)
        )

        self._decks = (
            ()
            if decks is None else
            (
                decks
                if isinstance(decks, tuple) else
                tuple(decks)
            )
        )

    @property
    def printings(self) -> FrozenMultiset[Printing]:
        return self._printings

    @property
    def decks(self) -> t.Tuple[Deck, ...]:
        return self._decks

    def __hash__(self) -> int:
        return hash(self._printings)

    def __eq__(self, other) -> bool:
        return isinstance(other, Pool) and other.printings == self.printings

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({len(self._printings)}, {len(self._decks)})'

    def serialize(self) -> serialization_model:
        return {
            'printings': self._printings,
            'decks': self._decks,
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> Pool:
        return Pool(
            inflator.inflate_all(Printing, value['printings']),
            (
                Deck.deserialize(_value, inflator)
                for _value in
                value.get('decks', ())
            ),
        )
