from __future__ import annotations

import typing as t

import datetime
from abc import abstractmethod, ABC

from immutabledict import immutabledict

from yeetlong.multiset import FrozenMultiset

from orp.models import OrpBase
from orp.relationships import Many

from mtgorp.models.persistent.attributes.expansiontype import ExpansionType
from mtgorp.models.persistent.attributes.typeline import TypeLine
from mtgorp.models.persistent.attributes.manacosts import ManaCost
from mtgorp.models.persistent.attributes.colors import Color
from mtgorp.models.persistent.attributes.powertoughness import PTValue, PowerToughness
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flags
from mtgorp.models.persistent.attributes.borders import Border


T = t.TypeVar('T')


class MtgModel(OrpBase):
    pass


class Artist(MtgModel):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def faces(self) -> t.AbstractSet[Face]:
        pass

    @property
    def printings(self) -> t.AbstractSet[Printing]:
        return frozenset(face.owner for face in self.faces)


class Card(MtgModel):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def type_line(self) -> t.Optional[TypeLine]:
        pass

    @property
    @abstractmethod
    def mana_cost(self) -> t.Optional[ManaCost]:
        pass

    @property
    @abstractmethod
    def color(self) -> t.AbstractSet[Color]:
        pass

    @property
    @abstractmethod
    def oracle_text(self) -> t.Optional[str]:
        pass

    @property
    @abstractmethod
    def power_toughness(self) -> t.Optional[PowerToughness]:
        pass

    @property
    @abstractmethod
    def loyalty(self) -> t.Optional[PTValue]:
        pass

    @property
    @abstractmethod
    def color_identity(self) -> t.Optional[t.AbstractSet[Color]]:
        pass

    @property
    def cmc(self) -> int:
        return self.mana_cost.cmc if self.mana_cost else 0

    @property
    @abstractmethod
    def cardboards(self) -> t.FrozenSet[Cardboard]:
        pass

    @property
    def cardboard(self) -> t.Optional[Cardboard]:
        try:
            return self.cardboards.__iter__().__next__()
        except StopIteration:
            return None


class Side(ABC):

    @property
    @abstractmethod
    def owner(self) -> Cardboard:
        pass

    @property
    @abstractmethod
    def cards(self) -> Many[Card]:
        pass


class Cardboard(MtgModel):
    _SPLIT_SEPARATOR = ' // '

    @property
    def id(self) -> str:
        return self.name

    @classmethod
    def calc_name(cls, names) -> str:
        return cls._SPLIT_SEPARATOR.join(names)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def printings(self) -> Many[Printing]:
        pass

    @property
    def printings_chronologically(self) -> t.Sequence[Printing]:
        return sorted(self.printings, key = lambda p: p.expansion.release_date)

    @property
    def expansions(self) -> t.AbstractSet[Expansion]:
        return frozenset(printing.expansion for printing in self.printings)

    @property
    @abstractmethod
    def front_cards(self) -> t.Sequence[Card]:
        pass

    @property
    @abstractmethod
    def back_cards(self) -> t.Sequence[Card]:
        pass

    @property
    def iter_cards(self) -> t.Iterator[Card]:
        for card in self.front_cards:
            yield card
        for card in self.back_cards:
            yield card

    @property
    def cards(self) -> t.Sequence[Card]:
        return tuple(self.iter_cards)

    @property
    @abstractmethod
    def layout(self) -> Layout:
        pass

    @property
    def front_card(self) -> Card:
        return self.front_cards.__iter__().__next__()

    @property
    def back_card(self) -> t.Optional[Card]:
        try:
            return self.back_cards.__iter__().__next__()
        except StopIteration:
            return None

    def from_expansion(self, expansion: t.Union[Expansion, str], allow_volatile: t.Optional[bool] = False) -> Printing:
        code = expansion.code if isinstance(expansion, Expansion) else expansion
        printings = [p for p in self.printings if p.expansion.code == code]
        if allow_volatile:
            return min(printings, key = lambda p: p.collector_number)
        else:
            if len(printings) > 1:
                raise RuntimeError(
                    f'{self} printed multiple times in {expansion}'
                )

            if printings:
                return printings[0]

        raise KeyError(
            '{} not printed in {}'.format(
                self,
                expansion,
            )
        )

    def from_block(self, block: t.Union[Block, str]) -> Printing:
        if isinstance(block, Block):
            for printing in self.printings:
                if printing.expansion.block == block:
                    return printing
        else:
            for printing in self.printings:
                if printing.expansion.block is not None and printing.expansion.block.name == block:
                    return printing

        raise KeyError(
            '{} not printed in {}'.format(
                self,
                block,
            )
        )

    @property
    def printing(self) -> Printing:
        return self.printings.__iter__().__next__()

    @property
    def original_printing(self) -> Printing:
        return sorted(
            self.printings,
            key = lambda printing:
            printing.expansion.release_date
        )[0]

    @property
    def latest_printing(self) -> Printing:
        return sorted(
            self.printings,
            key = lambda printing:
            printing.expansion.release_date
        )[-1]


class Face(MtgModel):

    @property
    @abstractmethod
    def artist(self) -> Artist:
        pass

    @property
    @abstractmethod
    def owner(self) -> Printing:
        pass

    @property
    @abstractmethod
    def flavor(self) -> str:
        pass


class Printing(MtgModel):

    @property
    @abstractmethod
    def cardboard(self) -> Cardboard:
        pass

    @property
    @abstractmethod
    def expansion(self) -> Expansion:
        pass

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def collector_number(self) -> int:
        pass

    @property
    @abstractmethod
    def collector_string(self) -> str:
        pass

    @property
    @abstractmethod
    def front_face(self) -> Face:
        pass

    @property
    @abstractmethod
    def back_face(self) -> Face:
        pass

    @property
    def faces(self) -> t.Tuple[Face, Face]:
        return self.front_face, self.back_face

    @property
    @abstractmethod
    def rarity(self) -> Rarity:
        pass

    @property
    @abstractmethod
    def in_booster(self) -> bool:
        pass

    @property
    @abstractmethod
    def flags(self) -> Flags:
        pass

    @property
    def border(self) -> t.Optional[Border]:
        return self.expansion.border

    def full_name(self) -> str:
        return f'{self.cardboard.name}|{self.expansion.code}'

    @property
    def alternative_printings(self) -> t.Iterator[Printing]:
        for printing in self.cardboard.printings:
            if printing != self:
                yield printing

    @property
    def alternative_printings_chronologically(self) -> t.Sequence[Printing]:
        return sorted(list(self.alternative_printings), key = lambda p: p.expansion.release_date)

    @property
    def scryfall_link(self) -> str:
        return f'https://scryfall.com/card/{self.expansion.code.lower()}/{self.collector_string}'

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.cardboard.name,
            self.expansion.code,
            self.id,
        )


class Expansion(MtgModel):
    _booster_map: t.Optional[BoosterMap]

    @property
    @abstractmethod
    def block(self) -> Block:
        pass

    @property
    @abstractmethod
    def printings(self) -> Many[Printing]:
        pass

    @property
    @abstractmethod
    def fragment_dividers(self) -> t.Sequence[int]:
        pass

    def fragmentize(self, frm: t.Union[int, None] = 0, to: t.Union[int, None] = None) -> ExpansionFragment:
        return ExpansionFragment(self, frm, to)

    @property
    def fragments(self) -> t.Tuple[ExpansionFragment, ...]:
        if self.fragment_dividers:
            fragments = []
            indexes = (0,) + tuple(self.fragment_dividers) + (None,)
            for i in range(len(indexes) - 1):
                fragments.append(self.fragmentize(indexes[i], indexes[i + 1]))
            return tuple(fragments)
        else:
            return self.fragmentize(0, None),

    def generate_booster(self) -> Booster:
        if getattr(self, '_booster_map', None) is None:
            setattr(self, '_booster_map', self.booster_key.get_booster_map(self.booster_expansion_collection))
        return self._booster_map.generate_booster()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def name_and_code(self) -> str:
        return f'[{self.code}] {self.name}'

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def expansion_type(self) -> ExpansionType:
        pass

    @property
    @abstractmethod
    def release_date(self) -> t.Optional[datetime.datetime]:
        pass

    @property
    @abstractmethod
    def booster_key(self) -> t.Optional[BoosterKey]:
        pass

    @property
    @abstractmethod
    def booster_expansion_collection(self) -> t.Optional[ExpansionCollection]:
        pass

    @property
    @abstractmethod
    def border(self) -> t.Optional[Border]:
        pass

    @property
    @abstractmethod
    def magic_card_info_code(self) -> t.Optional[str]:
        pass

    @property
    @abstractmethod
    def mkm_name(self) -> t.Optional[str]:
        pass

    @property
    @abstractmethod
    def mkm_id(self) -> t.Optional[int]:
        pass


class ExpansionFragment(object):

    def __init__(self, of: Expansion, frm: t.Union[int, None], to: t.Union[int, None]):
        self._of = of
        self._frm = frm
        self._to = to
        self._printings = set(sorted(of.printings, key = lambda printing: printing.collector_number)[frm:to])

    @property
    def of(self) -> Expansion:
        return self._of

    @property
    def frm(self) -> int:
        return self._frm

    @property
    def to(self) -> int:
        return self._to

    @property
    def printings(self) -> t.AbstractSet[Printing]:
        return self._printings


class Block(MtgModel):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def expansions(self) -> Many[Expansion]:
        pass

    @property
    def sets(self) -> t.Iterator[Expansion]:
        return filter(lambda e: e.expansion_type == ExpansionType.SET, self.expansions)

    @property
    def expansions_chronologically(self) -> t.List[Expansion]:
        return sorted(self.expansions, key = lambda expansion: expansion.release_date)

    @property
    def first_expansion(self) -> Expansion:
        return min(
            self.sets,
            key = lambda expansion: expansion.release_date,
        )


class Booster(t.Generic[T]):

    def __init__(self, items: t.Iterable[T], expansion: Expansion = None):
        pass

    @property
    @abstractmethod
    def items(self) -> FrozenMultiset[T]:
        pass

    @property
    def printings(self) -> FrozenMultiset[T]:
        return self.items

    @property
    @abstractmethod
    def expansion(self) -> t.Optional[Expansion]:
        pass

    @abstractmethod
    def __contains__(self, printing: T) -> bool:
        pass

    @abstractmethod
    def __iter__(self) -> t.Iterable[T]:
        pass


class ExpansionCollection(object):

    def __init__(
        self,
        main: Expansion,
        basics: t.Optional[Expansion] = None,
        premium: t.Optional[Expansion] = None,
        **expansions,
    ):
        expansions.update(
            {
                'main': main,
                'basics': main if basics is None else basics,
                'premium': main if premium is None else premium,
            }
        )
        self._expansions = immutabledict(expansions)

    @property
    def main(self) -> Expansion:
        return self._expansions['main']

    @property
    def basics(self) -> Expansion:
        return self._expansions['basics']

    @property
    def premium(self) -> Expansion:
        return self._expansions['premium']

    def __getitem__(self, item: str) -> Expansion:
        return self._expansions.__getitem__(item)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._expansions == other._expansions
        )

    def __hash__(self):
        return hash(self._expansions)

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            dict(self._expansions),
        )


class MapSlot(t.Generic[T]):
    options: FrozenMultiset[t.FrozenSet[T]]

    @abstractmethod
    def sample(self) -> T:
        pass

    @abstractmethod
    def sample_slot(self) -> t.FrozenSet[T]:
        pass


class BoosterMap(t.Generic[T]):

    @abstractmethod
    def generate_booster(self) -> Booster[T]:
        pass


class KeySlot(ABC):

    @abstractmethod
    def get_map_slot(self, expansion_collection: t.Union[ExpansionCollection, t.Collection[Printing]]) -> MapSlot:
        pass


class BoosterKey(ABC):
    slots: FrozenMultiset[KeySlot]

    @abstractmethod
    def get_booster_map(self, expansion_collection: ExpansionCollection) -> BoosterMap:
        pass
