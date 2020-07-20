from __future__ import annotations

import typing as t

from mtgorp.models.persistent.printing import Printing
from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator


class PrintingSet(Serializeable):

    def __init__(self, printings: t.Iterable[Printing]):
        self._printings = set(printings)

    def serialize(self) -> serialization_model:
        return {
            'printings': list(self._printings),
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> PrintingSet:
        return cls(inflator.inflate_all(Printing, value['printings']))

    def __hash__(self) -> int:
        return self._printings.__hash__()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._printings == other._printings
        )

    def __iter__(self) -> t.Iterator[Printing]:
        return self._printings.__iter__()
