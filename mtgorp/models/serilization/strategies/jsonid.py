import json

from mtgorp.models.serilization.serializeable import compacted_model
from mtgorp.models.serilization.strategies.strategy import Strategy


class JsonId(Strategy):

	@classmethod
	def _serialize(cls, model: compacted_model) -> str:
		return json.dumps(model)

	def _deserialize(self, s: str) -> compacted_model:
		return json.loads(s)