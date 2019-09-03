import typing as t

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import Strategy, S


class RawStrategy(Strategy):

    @classmethod
    def _serialize(cls, model: compacted_model) -> t.AnyStr:
        return model

    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        raise NotImplemented

    def deserialize(self, cls: t.Type[S], s: compacted_model) -> S:
        return cls.deserialize(s, self)

