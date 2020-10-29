import typing as t

from abc import abstractmethod

from orp.database import OrpBase

from mtgorp.db.database import CardDatabase
from mtgorp.models.serilization.serializeable import (
    Serializeable,
    Inflator,
    M,
    compacted_value,
    serialization_model,
    compacted_model,
    SerializationException,
)


S = t.TypeVar('S', bound = Serializeable)


class Strategy(Inflator):

    def __init__(self, db: CardDatabase):
        self._db: CardDatabase = db

    @classmethod
    def to_compacted_model(cls, serializeable: serialization_model) -> compacted_model:
        if isinstance(serializeable, OrpBase):
            return serializeable.primary_key

        if isinstance(serializeable, Serializeable):
            return cls.to_compacted_model(
                serializeable.serialize()
            )

        if isinstance(serializeable, compacted_value.__args__):
            return serializeable

        if isinstance(serializeable, dict):
            return {
                key:
                    cls.to_compacted_model(value)
                for key, value in
                serializeable.items()
            }

        return [
            cls.to_compacted_model(item)
            for item in
            serializeable
        ]

    def inflate(self, model_type: t.Type[M], key: t.Any) -> M:
        return self._db[model_type][key]

    @classmethod
    @abstractmethod
    def _serialize(cls, model: compacted_model) -> t.AnyStr:
        pass

    @classmethod
    def serialize(cls, serializeable: Serializeable) -> t.AnyStr:
        return cls._serialize(
            cls.to_compacted_model(
                serializeable.serialize()
            )
        )

    @abstractmethod
    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        pass

    def deserialize(self, cls: t.Type[S], s: t.AnyStr) -> S:
        try:
            return cls.deserialize(
                self._deserialize(s),
                self,
            )
        except KeyError:
            raise SerializationException()
