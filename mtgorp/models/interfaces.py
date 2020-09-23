from __future__ import annotations

import typing as t

import datetime
from abc import abstractmethod, ABC

from yeetlong.multiset import FrozenMultiset

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


class Artist(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def printings(self) -> t.Tuple[Printing, ...]:
        pass


class Card(ABC):

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
    @abstractmethod
    def cmc(self) -> int:
        pass

    @property
    @abstractmethod
    def cardboards(self) -> t.FrozenSet[Cardboard]:
        pass

    @property
    @abstractmethod
    def cardboard(self) -> t.Optional[Cardboard]:
        pass


class Side(ABC):

    @property
    @abstractmethod
    def owner(self) -> Cardboard:
        pass

    @property
    @abstractmethod
    def cards(self) -> Many[Card]:
        pass


class Cardboard(ABC):

    @property
    def id(self) -> str:
        return self.name

    @classmethod
    @abstractmethod
    def calc_name(cls, names) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def printings(self) -> Many[Printing]:
        pass

    @property
    @abstractmethod
    def front_cards(self) -> Many[Card]:
        pass

    @property
    @abstractmethod
    def back_cards(self) -> Many[Card]:
        pass

    @property
    @abstractmethod
    def cards(self) -> t.Tuple[Card, ...]:
        pass

    @property
    @abstractmethod
    def layout(self) -> Layout:
        pass

    @property
    @abstractmethod
    def front_card(self) -> Card:
        pass

    @property
    @abstractmethod
    def back_card(self) -> t.Optional[Card]:
        pass

    @property
    @abstractmethod
    def printing(self) -> Printing:
        pass

    @abstractmethod
    def from_expansion(self, expansion: t.Union[Expansion, str]) -> Printing:
        pass

    @abstractmethod
    def from_block(self, block: t.Union[Block, str]) -> Printing:
        pass

    @property
    @abstractmethod
    def original_printing(self) -> Printing:
        pass

    @property
    @abstractmethod
    def latest_printing(self) -> Printing:
        pass


class Face(ABC):

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


class Printing(ABC):

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
    def front_face(self) -> Face:
        pass

    @property
    @abstractmethod
    def back_face(self) -> Face:
        pass

    @property
    @abstractmethod
    def faces(self) -> t.Tuple[Face, Face]:
        pass

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
    @abstractmethod
    def border(self) -> t.Optional[Border]:
        pass


class Expansion(ABC):

    @property
    @abstractmethod
    def block(self) -> Block:
        pass

    @property
    @abstractmethod
    def printings(self) -> Many[Printing]:
        pass

    @abstractmethod
    def fragmentize(self, frm: t.Optional[int] = 0, to: t.Optional[int] = None) -> ExpansionFragment:
        pass

    @abstractmethod
    def generate_booster(self) -> Booster:
        pass

    @property
    @abstractmethod
    def fragments(self) -> t.Tuple[ExpansionFragment, ...]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def name_and_code(self) -> str:
        pass

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
    def release_date(self) -> t.Optional[datetime.date]:
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


class ExpansionFragment(Expansion):

    @property
    @abstractmethod
    def of(self) -> Expansion:
        pass

    @property
    @abstractmethod
    def frm(self) -> int:
        pass

    @property
    @abstractmethod
    def to(self) -> int:
        pass


class Block(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def expansions(self) -> Many[Expansion]:
        pass

    @property
    @abstractmethod
    def sets(self) -> t.Iterator[Expansion]:
        pass

    @property
    @abstractmethod
    def expansions_chronologically(self) -> t.List[Expansion]:
        pass

    @property
    @abstractmethod
    def first_expansion(self) -> Expansion:
        pass


class Booster(ABC):

    def __init__(self, printings: t.Iterable[Printing], expansion: Expansion = None):
        pass

    @property
    @abstractmethod
    def printings(self) -> FrozenMultiset[Printing]:
        pass

    @property
    @abstractmethod
    def sorted_printings(self) -> t.List[Printing]:
        pass

    @property
    @abstractmethod
    def expansion(self) -> t.Optional[Expansion]:
        pass

    @abstractmethod
    def __contains__(self, printing: Printing) -> bool:
        pass

    @abstractmethod
    def __iter__(self) -> t.Iterable[Printing]:
        pass


class ExpansionCollection(ABC):

    @property
    @abstractmethod
    def main(self) -> Expansion:
        pass

    @property
    @abstractmethod
    def basics(self) -> Expansion:
        pass

    @property
    @abstractmethod
    def premium(self) -> Expansion:
        pass

    @abstractmethod
    def __getitem__(self, item: str) -> Expansion:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __hash__(self):
        pass


class MapSlot(ABC):
    options: FrozenMultiset[t.FrozenSet[Printing]]

    @abstractmethod
    def sample(self) -> Printing:
        pass

    @abstractmethod
    def sample_slot(self) -> t.FrozenSet[Printing]:
        pass


class BoosterMap(ABC):

    @abstractmethod
    def generate_booster(self) -> Booster:
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
