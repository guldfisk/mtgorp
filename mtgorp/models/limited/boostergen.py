from __future__ import annotations

import itertools
import bisect
import random
import typing as t

from yeetlong.multiset import FrozenMultiset, BaseMultiset, Multiset

from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flag
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes import typeline
from mtgorp.models.interfaces import (
    Printing,
    BoosterKey as _BoosterKey,
    BoosterMap as _BoosterMap,
    KeySlot as _KeySlot,
    MapSlot as _MapSlot,
    ExpansionCollection,
)
from mtgorp.models.limited.booster import Booster
from mtgorp.tools.search.pattern import CriteriaBuilder, Criteria, Pattern
from mtgorp.tools.search.extraction import PrintingStrategy


def multiset_choice(ms: BaseMultiset):
    values, multiplicities = zip(*ms.items())
    cumulative_distribution = tuple(itertools.accumulate(multiplicities))
    return values[
        bisect.bisect_right(
            cumulative_distribution,
            random.random() * cumulative_distribution[-1]
        )
    ]


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


COMMON = Option(CriteriaBuilder().rarity.equals(Rarity.COMMON).type_line.contains.no(typeline.BASIC).all())
UNCOMMON = Option(CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).all())
RARE = Option(CriteriaBuilder().rarity.equals(Rarity.RARE).all())
MYTHIC = Option(CriteriaBuilder().rarity.equals(Rarity.MYTHIC).all())
SPECIAL = Option(CriteriaBuilder().rarity.equals(Rarity.SPECIAL).all())
TIMESHIFTED_COMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.COMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_UNCOMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_RARE = Option(
    CriteriaBuilder().rarity.equals(Rarity.RARE).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_MYTHIC = Option(
    CriteriaBuilder().rarity.equals(Rarity.MYTHIC).flags.contains(Flag.TIMESHIFTED).all(),
)
DOUBLEFACED_COMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.COMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_UNCOMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_RARE = Option(
    CriteriaBuilder().rarity.equals(Rarity.RARE).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_MYTHIC = Option(
    CriteriaBuilder().rarity.equals(Rarity.MYTHIC).layout.equals(Layout.TRANSFORM).all(),
)
PREMIUM = Option(
    CriteriaBuilder().all(),
    'premium',
)
BASIC = Option(
    CriteriaBuilder().type_line.contains(typeline.BASIC).all(),
    'basics',
)
DRAFT_MATTERS_COMMON = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.COMMON).all(),
)
DRAFT_MATTERS_UNCOMMON = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.UNCOMMON).all(),
)
DRAFT_MATTERS_RARE = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.RARE).all(),
)
DRAFT_MATTERS_MYTHIC = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.MYTHIC).all(),
)


class KeySlot(_KeySlot):

    def __init__(self, options: t.Iterable[Option]):
        self._options: FrozenMultiset[Option] = (
            options
            if isinstance(options, FrozenMultiset) else
            FrozenMultiset(options)
        )

    def get_map_slot(self, expansion_collection: t.Union[ExpansionCollection, t.Collection[Printing]]) -> MapSlot:
        return MapSlot(
            {
                frozenset(
                    printing
                        for printing in
                        (
                            expansion_collection[option.collection_key].printings
                            if isinstance(expansion_collection, ExpansionCollection) else
                            expansion_collection
                        )
                        if printing.in_booster and option.pattern.match(printing)
                ):
                    weight
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
            dict(self._options.elements()),
        )


COMMON_SLOT = KeySlot((COMMON,))
UNCOMMON_SLOT = KeySlot((UNCOMMON,))
RARE_SLOT = KeySlot((RARE,))
MYTHIC_SLOT = KeySlot((MYTHIC,))
SPECIAL_SLOT = KeySlot((SPECIAL,))
RARE_MYTHIC_SLOT = KeySlot(
    {
        RARE: 7,
        MYTHIC: 1,
    }
)
PREMIUM_SLOT = KeySlot((PREMIUM,))
BASIC_SLOT = KeySlot((BASIC,))


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

    def get_booster_map(self, expansion_collection: t.Union[ExpansionCollection, t.Collection[Printing]]) -> BoosterMap:
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
            self._slots.items(),
        )


class MapSlot(_MapSlot):

    def __init__(self, options: t.Iterable[t.FrozenSet[Printing]]):
        self.options = options if isinstance(options, FrozenMultiset) else FrozenMultiset(options)

    def sample(self) -> Printing:
        return random.choice(
            multiset_choice(
                self.options
            )
        )

    def sample_slot(self) -> t.FrozenSet[Printing]:
        return multiset_choice(self.options)

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}: {}'.format(len(option), multiplicity) for option, multiplicity in self.options.items()),
        )


class BoosterMap(_BoosterMap):

    def __init__(self, slots: t.Iterable[MapSlot]):
        self.slots = slots if isinstance(slots, FrozenMultiset) else FrozenMultiset(slots)

    def generate_booster(self) -> Booster:
        slots = Multiset(slot.sample_slot() for slot in self.slots)
        printings = Multiset()

        for value, multiplicity in slots.items():
            try:
                printings.update(
                    random.sample(
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
            self.slots,
        )
