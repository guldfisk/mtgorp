from __future__ import annotations

import typing as t

from abc import abstractmethod, ABC

from yeetlong.multiset import Multiset

from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.printing import Printing
from mtgorp.models.persistent.attributes import typeline
from mtgorp.tools.search.pattern import Criteria, CriteriaBuilder, All, Not, Any, Contains
from mtgorp.tools.search.extraction import ExtractionStrategy, CardboardStrategy, PrintingStrategy, TypeLineExtractor


T = t.TypeVar('T')


class Category(object):

    def __init__(
        self,
        name: str,
        criteria: Criteria,
    ):
        self._name = name
        self._criteria = criteria

    @property
    def name(self) -> str:
        return self._name

    @property
    def criteria(self) -> Criteria:
        return self._criteria

    def __hash__(self) -> int:
        return hash((self._name, self._criteria))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self._name == other._name
            and self._criteria == other._criteria
        )


class Groupifyer(ABC, t.Generic[T]):

    def __init__(
        self,
        name: str,
        categories: t.Iterable[Category],
        include_others: bool = True,
    ):
        self._name = name
        self._categories: t.List[Category] = list(categories)
        self._include_others = include_others

    @property
    @abstractmethod
    def _extraction_strategy(self) -> t.Type[ExtractionStrategy[T]]:
        pass

    @abstractmethod
    def _group_type(self) -> t.Type[Group[T]]:
        pass

    def groupify(self, items: t.Iterable[T]) -> Grouping[T]:

        items = Multiset(items)

        categories = []

        for category in self._categories:
            matches = Multiset(category.criteria.matches(items, self._extraction_strategy))
            categories.append(self._group_type()(category.name, matches))

            items -= matches

        if items and self._include_others:
            categories.append(self._group_type()('Others', items))

        return Grouping(self._name, categories)


class Group(t.Generic[T]):

    def __init__(self, name: str, items: t.Iterable[T]):
        self._name = name
        self._items: Multiset[T] = Multiset(items)

    @abstractmethod
    def _item_to_string(self, item: T, multiplicity: int) -> str:
        pass

    @property
    @abstractmethod
    def _sorted_items(self) -> t.List[t.Tuple[T, int]]:
        pass

    def _items_to_string(self) -> str:
        return '\n'.join(
            self._item_to_string(item, multiplicity)
            for item, multiplicity in
            self._sorted_items
        )

    def __str__(self) -> str:
        return f'{self._name}: {len(self._items)}\n{self._items_to_string()}'

    def __len__(self) -> int:
        return self._items.__len__()


class Grouping(t.Generic[T]):

    def __init__(self, name: str, groups: t.Iterable[Group[T]]):
        self._name = name
        self._groups = groups

    def __str__(self) -> str:
        return f'{self._name}: {len(self)}\n\n' + '\n\n'.join(
            group.__str__()
            for group in
            self._groups
        )

    def __len__(self) -> int:
        return sum(len(group) for group in self._groups)


class CardboardGroup(Group[Cardboard]):

    def _item_to_string(self, item: Cardboard, multiplicity: int) -> str:
        return f'{multiplicity} {item.name}'

    @property
    def _sorted_items(self) -> t.List[t.Tuple[Cardboard, int]]:
        return sorted(self._items.items(), key = lambda item: item[0].name)


class PrintingGroup(Group[Printing]):

    def _item_to_string(self, item: Printing, multiplicity: int) -> str:
        return f'{multiplicity} [{"" if item.expansion is None else item.expansion.code}] {item.cardboard.name}'

    @property
    def _sorted_items(self) -> t.List[t.Tuple[Printing, int]]:
        return sorted(self._items.items(), key = lambda item: item[0].cardboard.name)


class CardboardGroupifyer(Groupifyer[Cardboard]):

    @property
    def _extraction_strategy(self) -> t.Type[ExtractionStrategy[T]]:
        return CardboardStrategy

    def _group_type(self) -> t.Type[Group[T]]:
        return CardboardGroup


class PrintingGroupifyer(Groupifyer[Printing]):

    @property
    def _extraction_strategy(self) -> t.Type[ExtractionStrategy[T]]:
        return PrintingStrategy

    def _group_type(self) -> t.Type[Group[T]]:
        return PrintingGroup


CREATURE_CATEGORY = Category(
    'Creatures',
    CriteriaBuilder().type_line.contains(typeline.CREATURE).all(),
)

INSTANT_SORCERY_CATEGORY = Category(
    'Instant & Sorcery',
    CriteriaBuilder().type_line.contains(typeline.INSTANT).type_line.contains(typeline.SORCERY).any(),
)

NON_CREATURE_NON_LAND_PERMANENT_CATEGORY = Category(
    'Non-Creature Permanents',
    All(
        {
            Not(
                Any(
                    {
                        Contains(TypeLineExtractor, typeline.CREATURE),
                        Contains(TypeLineExtractor, typeline.LAND),
                    }
                )
            ),
            Any(
                {
                    Contains(TypeLineExtractor, typeline.ARTIFACT),
                    Contains(TypeLineExtractor, typeline.ENCHANTMENT),
                    Contains(TypeLineExtractor, typeline.PLANESWALKER),
                }
            ),
        }
    ),
)

LANDS_CATEGORY = Category(
    'Lands',
    CriteriaBuilder().type_line.contains(typeline.LAND).all(),
)

STANDARD_PRINTING_GROUPIFYER = PrintingGroupifyer(
    'Deck',
    (
        CREATURE_CATEGORY,
        INSTANT_SORCERY_CATEGORY,
        NON_CREATURE_NON_LAND_PERMANENT_CATEGORY,
        LANDS_CATEGORY,
    ),
)
