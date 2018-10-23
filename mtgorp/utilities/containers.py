import typing as t

from multiset import FrozenMultiset
from multiset import Multiset as _Multiset

T = t.TypeVar('T')


class HashableMultiset(FrozenMultiset, t.Generic[T]):
	
	def __hash__(self):
		return hash(frozenset(self._elements.items()))

	def __iter__(self) -> t.Iterator[T]:
		return super().__iter__()

	def __getitem__(self, item: T) -> int:
		return super().__getitem__(item)


class Multiset(_Multiset, t.Generic[T]):

	def __iter__(self) -> t.Iterator[T]:
		return super().__iter__()

	def items(self) -> t.Iterable[t.Tuple[T, int]]:
		return super().items()
