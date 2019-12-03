import typing as t

import json

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import Strategy


class JsonId(Strategy):

    @classmethod
    def _serialize(cls, model: compacted_model) -> t.AnyStr:
        return json.dumps(model)

    def _deserialize(self, s: t.AnyStr) -> compacted_model:
        return json.loads(s)
