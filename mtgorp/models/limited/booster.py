import typing as t

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.interfaces import Printing, Expansion, T
from mtgorp.models.interfaces import Booster as _Booster


class Booster(_Booster[T]):

    def __init__(self, items: t.Iterable[T], expansion: Expansion = None):
        self._items = items if isinstance(items, FrozenMultiset) else FrozenMultiset(items)
        self._expansion = expansion

    @property
    def items(self) -> FrozenMultiset[T]:
        return self._items

    @property
    def expansion(self) -> t.Optional[Expansion]:
        return self._expansion

    def __str__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            self._items.dict_string(),
        )

    def __contains__(self, printing: T) -> bool:
        return printing in self._items

    def __iter__(self) -> t.Iterator[T]:
        return self._items.__iter__()

    def __len__(self) -> int:
        return len(self._items)


class PrintingsBooster(Booster[Printing]):

    @property
    def sorted_printings(self) -> t.List[Printing]:
        return sorted(self._items, key = lambda p: p.rarity.value, reverse = True)

    def __str__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(a_printing.cardboard.name for a_printing in self.sorted_printings),
        )
