import typing as t

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import Strategy


class RawStrategy(Strategy):

    @classmethod
    def _serialize(cls, model: compacted_model) -> t.AnyStr:
        return model

    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        raise NotImplemented