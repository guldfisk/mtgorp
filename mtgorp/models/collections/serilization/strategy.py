import typing as t

from abc import ABC, abstractmethod
import json

from mtgorp.db.database import CardDatabase
from mtgorp.models.interfaces import Printing
from mtgorp.models.collections.serilization.serializeable import (
	Serializeable,
	model_tree,
	id_tree,
	SerializationException,
)


S = t.TypeVar('S', bound=Serializeable)


class Strategy(ABC):

	def __init__(self, db: CardDatabase):
		self._db = db #type: CardDatabase

	@classmethod
	def _models_to_ids(cls, tree: model_tree) -> id_tree:
		return {
			key:
				value
				if isinstance(value, str) else
				[
					item.id
					if isinstance(item, Printing) else
					(
						cls._models_to_ids(item)
						if isinstance(item, dict) else
						item
					)
					for item in
					value
				]
				for key, value in
				tree.items()
		}

	def _ids_to_models(self, tree: id_tree) -> model_tree:
		return {
			key:
				value
				if isinstance(value, str) else
				[
					self._db.printings[item]
					if isinstance(item, int) else
					(
						self._ids_to_models(item)
						if isinstance(item, dict) else
						item
					)
					for item in
					value
				]
			for key, value in
			tree.items()
		}


	@classmethod
	@abstractmethod
	def serialize(cls, serializeable: Serializeable) -> str:
		pass

	@abstractmethod
	def _deserialize(self, s: str) -> model_tree:
		pass

	def deserialize(self, cls: t.Type[S], s: str) -> S:
		try:
			return cls.from_model_tree(
				self._deserialize(s)
			)
		except KeyError:
			raise SerializationException()


class JsonId(Strategy):

	@classmethod
	def serialize(cls, serializeable: Serializeable) -> str:
		return json.dumps(
			cls._models_to_ids(
				serializeable.to_model_tree()
			)
		)

	def _deserialize(self, s: str) -> model_tree:
		return self._ids_to_models(
			json.loads(s)
		)
