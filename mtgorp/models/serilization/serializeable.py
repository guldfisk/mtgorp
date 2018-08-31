import typing as t

from abc import ABC, abstractmethod

from orp.database import Model


compacted_value = t.Union[int, str, bool, float, None]
serializeable_value = t.Union[compacted_value, Model, 'Serializeable']

compacted_model = t.Union[
	compacted_value,
	t.List[t.Union[compacted_value, t.List, t.Dict]],
	t.Dict[str, t.Union[compacted_value, t.List, t.Dict]],
]

serialization_model = t.Union[
	serializeable_value,
	t.Iterable[t.Union[serializeable_value, t.Iterable, t.Dict]],
	t.Dict[str, t.Union[serializeable_value, t.Iterable, t.Dict]],
]


M = t.TypeVar('M', bound=Model)


class Inflator(ABC):

	@abstractmethod
	def inflate(self, model_type: t.Type[M], key: t.Any) -> M:
		pass

	def inflate_all(self, model_type: t.Type[M], keys: t.Iterable[t.Any]) -> t.Iterable[M]:
		return (self.inflate(model_type, key) for key in keys)


class SerializationException(Exception):
	pass


class Serializeable(ABC):

	@abstractmethod
	def serialize(self) -> serialization_model:
		pass

	@classmethod
	@abstractmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Serializeable':
		pass

	@abstractmethod
	def __hash__(self) -> int:
		return super().__hash__()

	@abstractmethod
	def __eq__(self, other: object) -> bool:
		return super().__eq__(other)

