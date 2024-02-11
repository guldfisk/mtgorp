import typing as t

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import S, Strategy


class RawStrategy(Strategy):
    @classmethod
    def _serialize(cls, model: compacted_model) -> compacted_model:
        return model

    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        raise NotImplementedError()

    def deserialize(self, cls: t.Type[S], s: compacted_model) -> S:
        return cls.deserialize(s, self)
