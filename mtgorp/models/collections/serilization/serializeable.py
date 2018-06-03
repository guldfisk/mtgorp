import typing as t

from abc import ABC, abstractmethod

from mtgorp.models.interfaces import Printing


model_tree = t.Dict[str, t.Union[str, t.Iterable[t.Union[Printing, t.Dict, str]]]]
id_tree = t.Dict[str, t.Union[str, t.Iterable[t.Union[int, t.Dict, str]]]]


class SerializationException(Exception):
	pass


class Serializeable(ABC):

	@abstractmethod
	def to_model_tree(self) -> model_tree:
		pass

	@classmethod
	@abstractmethod
	def from_model_tree(cls, tree: model_tree) -> 'Serializeable':
		pass