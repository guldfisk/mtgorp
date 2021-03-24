from __future__ import annotations

import itertools
import bisect
import random
import typing as t

import numpy as np

from yeetlong.multiset import FrozenMultiset, BaseMultiset, Multiset

from mtgorp.models.interfaces import (
    Printing,
    BoosterKey as _BoosterKey,
    BoosterMap as _BoosterMap,
    KeySlot as _KeySlot,
    MapSlot as _MapSlot,
    ExpansionCollection,
)
from mtgorp.models.limited.booster import Booster
from mtgorp.tools.search.extraction import PrintingStrategy
from mtgorp.tools.search.pattern import Criteria, Pattern


T = t.TypeVar('T')


def multiset_choice(ms: BaseMultiset[T]) -> T:
    values, multiplicities = zip(*ms.items())
    cumulative_distribution = tuple(itertools.accumulate(multiplicities))
    return values[
        bisect.bisect_right(
            cumulative_distribution,
            random.random() * cumulative_distribution[-1]
        )
    ]


def multiset_sample(ms: BaseMultiset[T], amount: int) -> t.List[T]:
    items, probabilities = zip(*ms.items())
    probabilities = np.asarray(probabilities)
    return np.random.choice(items, amount, replace = False, p = probabilities / sum(probabilities))


class GenerateBoosterException(Exception):
    pass


class Option(object):

    def __init__(self, criteria: Criteria, collection_key: str = 'main'):
        self._pattern = Pattern(criteria, PrintingStrategy)
        self._collection_key = collection_key

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @property
    def collection_key(self):
        return self._collection_key

    def __hash__(self):
        return hash((self.__class__, self._pattern, self._collection_key))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self._pattern == other._pattern
            and self._collection_key == other._collection_key
        )

    def __repr__(self) -> str:
        return '{}({}, {})'.format(
            self.__class__.__name__,
            self._pattern,
            self._collection_key,
        )


class KeySlot(_KeySlot):

    def __init__(self, options: t.Iterable[Option]):
        self._options: FrozenMultiset[Option] = (
            options
            if isinstance(options, FrozenMultiset) else
            FrozenMultiset(options)
        )

    def get_map_slot(self, expansion_collection: t.Union[ExpansionCollection, t.Collection[Printing]]) -> MapSlot[Printing]:
        return MapSlot(
            {
                FrozenMultiset(
                    printing
                    for printing in
                    (
                        expansion_collection[option.collection_key].printings
                        if isinstance(expansion_collection, ExpansionCollection) else
                        expansion_collection
                    )
                    if printing.in_booster and option.pattern.match(printing)
                ): weight
                for option, weight in
                self._options.items()
            }
        )

    def __hash__(self):
        return hash((self.__class__, self._options))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._options == other._options

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            self._options.dict_string(),
        )


class BoosterKey(_BoosterKey):

    def __init__(self, slots: t.Iterable[KeySlot]):
        self._slots: FrozenMultiset[KeySlot] = (
            slots
            if isinstance(slots, FrozenMultiset) else
            FrozenMultiset(slots)
        )

    @property
    def slots(self) -> FrozenMultiset[KeySlot]:
        return self._slots

    def get_booster_map(self, expansion_collection: t.Union[ExpansionCollection, t.Collection[Printing]]) -> BoosterMap[Printing]:
        return BoosterMap(
            {
                slot.get_map_slot(expansion_collection): multiplicity
                for slot, multiplicity in
                self.slots.items()
            }
        )

    def __hash__(self):
        return hash((self.__class__, self._slots))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._slots == other.slots

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self._slots.dict_string(),
        )


class MapSlot(_MapSlot[T]):

    def __init__(self, options: t.Mapping[FrozenMultiset[T], int]):
        self.options: FrozenMultiset[FrozenMultiset[T]] = (
            options
            if isinstance(options, FrozenMultiset) else
            FrozenMultiset(options)
        )

    def sample(self) -> T:
        return multiset_choice(
            multiset_choice(
                self.options
            )
        )

    def sample_slot(self) -> FrozenMultiset[T]:
        return multiset_choice(self.options)

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}: {}'.format(len(option), multiplicity) for option, multiplicity in self.options.items()),
        )


class BoosterMap(_BoosterMap[T]):

    def __init__(self, slots: t.Iterable[MapSlot[T]]):
        self.slots: FrozenMultiset[MapSlot] = slots if isinstance(slots, FrozenMultiset) else FrozenMultiset(slots)

    def generate_booster(self) -> Booster[T]:
        slots = Multiset(slot.sample_slot() for slot in self.slots)
        printings = Multiset()

        for value, multiplicity in slots.items():
            try:
                printings.update(
                    multiset_sample(
                        value,
                        multiplicity,
                    )
                )
            except ValueError:
                raise GenerateBoosterException('Not enough printings')

        return Booster(printings)

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            self.slots.dict_string(),
        )
