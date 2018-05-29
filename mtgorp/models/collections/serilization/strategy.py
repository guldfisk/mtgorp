import typing as t

from abc import ABC, abstractmethod
import json

from mtgorp.db.database import CardDatabase
from mtgorp.models.interfaces import Printing, Cardboard
from mtgorp.models.collections.serilization.serializeable import Serializeable, model_tree, id_tree


S = t.TypeVar('S', bound=Serializeable)


class Strategy(ABC):

	def __init__(self, db: CardDatabase):
		self._db = db #type: CardDatabase

	@classmethod
	@abstractmethod
	def serialize(cls, serializeable: Serializeable) -> str:
		pass

	@abstractmethod
	def deserialize(self, cls: t.Type[Serializeable], s: str) -> Serializeable:
		pass


class JsonId(Strategy):

	@classmethod
	def _serialize(cls, tree: model_tree) -> id_tree:
		return {
			key: [
				item.id
				if isinstance(item, Printing)
				else cls._serialize(item)
				for item in
				value
			]
			for key, value in
			tree.items()
		}

	@classmethod
	def serialize(cls, serializeable: Serializeable) -> str:
		return json.dumps(
			cls._serialize(
				serializeable.to_model_tree()
			)
		)

	def _deserialize(self, tree: id_tree) -> model_tree:
		return {
			key: [
				self._db.printings[item]
				if isinstance(item, int)
				else self._deserialize(item)
				for item in
				value
			]
			for key, value in
			tree.items()
		}

	def deserialize(self, cls: t.Type[S], s: str) -> S:
		return cls.from_model_tree(
			self._deserialize(
				json.loads(s)
			)
		)
