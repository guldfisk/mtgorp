import typing as t

from multiset import FrozenMultiset
from multiset import Multiset as _Multiset

T = t.TypeVar('T')


class HashableMultiset(FrozenMultiset, t.Generic[T]):
	_hash = None #type: int

	def __init__(self, iterable=None):
		super().__init__(iterable)

	def __hash__(self):
		if hasattr(self, '_hash') or self._hash is None:
			self._hash = hash(frozenset(self._elements.items()))
		return self._hash

	def __iter__(self) -> t.Iterator[T]:
		return super().__iter__()

	def __getitem__(self, item: T) -> int:
		return super().__getitem__(item)


class Multiset(_Multiset, t.Generic[T]):

	def __iter__(self) -> t.Iterator[T]:
		return super().__iter__()

	def items(self) -> t.Iterable[t.Tuple[T, int]]:
		return super().items()
