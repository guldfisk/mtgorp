from __future__ import annotations

import typing as t

from mtgorp.models.interfaces import Printing
from mtgorp.models.serilization.serializeable import (
    Inflator,
    PersistentHashable,
    Serializeable,
    serialization_model,
)


class PrintingSet(Serializeable, PersistentHashable):
    def __init__(self, printings: t.Iterable[Printing]):
        self._printings = frozenset(printings)

    def serialize(self) -> serialization_model:
        return {
            "printings": list(self._printings),
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> PrintingSet:
        return cls(inflator.inflate_all(Printing, value["printings"]))

    def __hash__(self) -> int:
        return self._printings.__hash__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self._printings == other._printings

    def __iter__(self) -> t.Iterator[Printing]:
        return self._printings.__iter__()

    def _calc_persistent_hash(self) -> t.Iterator[t.ByteString]:
        for printing in sorted(self._printings, key=lambda _printing: _printing.id):
            yield str(printing.id).encode("ASCII")
