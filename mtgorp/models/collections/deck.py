from __future__ import annotations

import typing as t
from abc import abstractmethod

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.interfaces import Cardboard, Printing
from mtgorp.models.serilization.serializeable import (
    Inflator,
    Serializeable,
    serialization_model,
)


Deckable = t.Union[Printing, Cardboard]
D = t.TypeVar("D", bound=Deckable)


class BaseDeck(t.Generic[D], Serializeable):
    _maindeck: FrozenMultiset[D]

    def __init__(
        self,
        maindeck: t.Union[t.Iterable[D], t.Iterable[t.Tuple[D, int]]],
        sideboard: t.Union[t.Iterable[D], t.Iterable[t.Tuple[D, int]], None] = None,
    ):
        self._maindeck: FrozenMultiset[D] = (
            maindeck if isinstance(maindeck, FrozenMultiset) else FrozenMultiset(maindeck)
        )

        self._sideboard: FrozenMultiset[D] = (
            (sideboard if isinstance(sideboard, FrozenMultiset) else FrozenMultiset(sideboard))
            if sideboard is not None
            else FrozenMultiset()
        )

    @property
    def maindeck(self) -> FrozenMultiset[D]:
        return self._maindeck

    @property
    def sideboard(self) -> FrozenMultiset[D]:
        return self._sideboard

    @property
    def seventy_five(self) -> FrozenMultiset[D]:
        return self._maindeck + self._sideboard

    def __iter__(self) -> t.Iterable[D]:
        return self.seventy_five.__iter__()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._maindeck == other.maindeck
            and self._sideboard == other.sideboard
        )

    def __hash__(self) -> int:
        return hash(self.seventy_five)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self._maindeck)}, {len(self._sideboard)})"

    def serialize(self) -> serialization_model:
        return {
            "maindeck": list(self._maindeck),
            "sideboard": list(self._sideboard),
        }

    @classmethod
    @abstractmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> BaseDeck:
        pass


class CardboardDeck(BaseDeck[Cardboard]):
    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> BaseDeck:
        return cls(
            inflator.inflate_all(Cardboard, value["maindeck"]),
            inflator.inflate_all(Cardboard, value.get("sideboard", ())),
        )


class Deck(BaseDeck[Printing]):
    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> Deck:
        return cls(
            inflator.inflate_all(Printing, value["maindeck"]),
            inflator.inflate_all(Printing, value.get("sideboard", ())),
        )

    @property
    def as_cardboards(self):
        return CardboardDeck(
            FrozenMultiset(p.cardboard for p in self._maindeck),
            FrozenMultiset(p.cardboard for p in self._sideboard),
        )
