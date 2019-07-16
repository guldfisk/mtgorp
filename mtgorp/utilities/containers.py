import typing as t
from collections import Counter as _Counter
from typing import ItemsView, Mapping as Mapping, Tuple, Optional, List

from multiset import FrozenMultiset, Multiset as _Multiset


T = t.TypeVar('T')


class Counter(_Counter, t.Generic[T]):

    def __init__(self, mapping: t.Optional[t.Mapping[T, int]] = None) -> None:
        if mapping is None:
            super().__init__({})
        else:
            super().__init__(mapping)

    def __getitem__(self, k: T) -> int:
        return super().__getitem__(k)

    def items(self) -> ItemsView[T, int]:
        return super().items()

    def update(self, mapping: Mapping[T, int], **kwargs: int) -> None:
        super().update(mapping, **kwargs)

    def subtract(self, mapping: Mapping[T, int]) -> None:
        super().subtract(mapping)

    def most_common(self, n: Optional[int] = ...) -> List[Tuple[T, int]]:
        return super().most_common(n)


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

    def combine_with_counter(self, other: _Counter) -> 'HashableMultiset':
        result = self.__copy__()
        _elements = result._elements
        _total = result._total
        for element, multiplicity in other.items():
            old_multiplicity = _elements.get(element, 0)
            new_multiplicity = old_multiplicity + multiplicity
            if old_multiplicity > 0 and new_multiplicity <= 0:
                del _elements[element]
                _total -= old_multiplicity
            elif new_multiplicity > 0:
                _elements[element] = new_multiplicity
                _total += multiplicity
        result._total = _total
        return result

    def __add__(self, other):
        if isinstance(other, _Counter):
            return self.combine_with_counter(other)
        return super().__add__(other)


class Multiset(_Multiset, t.Generic[T]):

    def __iter__(self) -> t.Iterator[T]:
        return super().__iter__()

    def items(self) -> t.Iterable[t.Tuple[T, int]]:
        return super().items()
