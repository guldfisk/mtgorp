import typing as t

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.interfaces import Printing, Expansion
from mtgorp.models.interfaces import Booster as _Booster


class Booster(_Booster):

    def __init__(self, printings: t.Iterable[Printing], expansion: Expansion = None):
        self._printings = printings if isinstance(printings, FrozenMultiset) else FrozenMultiset(printings)
        self._expansion = expansion

    @property
    def printings(self) -> FrozenMultiset[Printing]:
        return self._printings

    @property
    def sorted_printings(self) -> t.List[Printing]:
        return sorted(self._printings, key = lambda p: p.rarity.value, reverse = True)

    @property
    def expansion(self) -> t.Optional[Expansion]:
        return self._expansion

    def __str__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(a_printing.cardboard.name for a_printing in self.sorted_printings),
        )

    def __contains__(self, printing: Printing) -> bool:
        return printing in self._printings

    def __iter__(self) -> t.Iterator[Printing]:
        return self._printings.__iter__()

    def __len__(self) -> int:
        return len(self._printings)
