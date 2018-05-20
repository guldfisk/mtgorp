import typing as t

from multiset import FrozenMultiset

T = t.TypeVar('T')


class HashableMultiset(FrozenMultiset, t.Generic[T]):
	
	def __hash__(self):
		return hash(frozenset(self._elements.items()))

	def __iter__(self) -> t.Iterator[T]:
		return super().__iter__()
