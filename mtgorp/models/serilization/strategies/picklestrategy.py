import typing as t

import pickle

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import Strategy


class PickleStrategy(Strategy):

    @classmethod
    def _serialize(cls, model: compacted_model) -> t.AnyStr:
        return pickle.dumps(model)

    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        return pickle.loads(s)
