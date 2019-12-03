from __future__ import annotations

import typing as t
import hashlib

from abc import ABC, abstractmethod

from orp.database import Model


compacted_value = t.Union[int, str, bool, float, None]
serializeable_value = t.Union[compacted_value, Model, 'Serializeable']

compacted_model = t.Union[
    compacted_value,
    t.List[t.Union[compacted_value, t.List, t.Mapping]],
    t.Mapping[str, t.Union[compacted_value, t.List, t.Mapping]],
]

serialization_model = t.Union[
    serializeable_value,
    t.Iterable[t.Union[serializeable_value, t.Iterable, t.Mapping]],
    t.Mapping[str, t.Union[serializeable_value, t.Iterable, t.Mapping]],
]


M = t.TypeVar('M', bound=Model)


class Inflator(ABC):

    @abstractmethod
    def inflate(self, model_type: t.Type[M], key: t.Any) -> M:
        pass

    def inflate_all(self, model_type: t.Type[M], keys: t.Iterable[t.Any]) -> t.Iterable[M]:
        return (self.inflate(model_type, key) for key in keys)


class SerializationException(Exception):
    pass


class Serializeable(ABC):

    @abstractmethod
    def serialize(self) -> serialization_model:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> Serializeable:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        return super().__hash__()

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)


class PersistentHashable(ABC):
    
    @abstractmethod
    def _calc_persistent_hash(self) -> t.Iterable[t.ByteString]:
        pass
    
    def persistent_hash(self) -> str:
        if hasattr(self, '_persistent_hash'):
            return getattr(self, '_persistent_hash')

        hasher = hashlib.sha512()
        for s in self._calc_persistent_hash():
            hasher.update(s)

        setattr(self, '_persistent_hash', hasher.hexdigest())

        return getattr(self, '_persistent_hash')
