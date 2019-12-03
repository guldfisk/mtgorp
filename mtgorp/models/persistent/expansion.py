from __future__ import annotations

import datetime
import typing as t

from lazy_property import LazyProperty

from orp.relationships import Many, One, OneDescriptor
from orp.database import Model, PrimaryKey

from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.models.interfaces import Block, BoosterKey, ExpansionCollection, Booster, Printing
from mtgorp.models.interfaces import Expansion as _Expansion
from mtgorp.models.interfaces import ExpansionFragment as _ExpansionFragment


class Expansion(Model, _Expansion):
    primary_key = PrimaryKey('code')
    _code: str

    def __init__(
        self,
        code: str,
        name: str = None,
        block: Block = None,
        release_date: datetime.date = None,
        booster_key: BoosterKey = None,
        booster_expansion_collection: ExpansionCollection = None,
        border: Border = None,
        magic_card_info_code: str = None,
        mkm_name: str = None,
        mkm_id: int = None,
        fragment_dividers: t.Tuple[int, ...] = (),
    ):
        self._name = name
        self._block = One(self, 'expansions', block)
        self._release_date = release_date
        self._booster_key = booster_key
        self._booster_expansion_collection = booster_expansion_collection
        self._border = border
        self._magic_card_info_code = magic_card_info_code
        self._mkm_name = mkm_name
        self._mkm_id = mkm_id
        self._fragment_dividers = fragment_dividers
        self._booster_map = None

        self._printings = Many(self, '_expansion')

    block: Block = OneDescriptor('_block')

    @property
    def printings(self) -> Many[Printing]:
        return self._printings

    def fragmentize(self, frm: t.Union[int, None] = 0, to: t.Union[int, None] = None) -> ExpansionFragment:
        return ExpansionFragment(self, frm, to)

    def generate_booster(self) -> Booster:
        if self._booster_map is None:
            self._booster_map = self._booster_key.get_booster_map(self._booster_expansion_collection)
        return self._booster_map.generate_booster()

    @LazyProperty
    def fragments(self) -> t.Tuple[ExpansionFragment, ...]:
        if self._fragment_dividers:
            fragments = []
            indexes = (0,) + self._fragment_dividers + (None,)
            for i in range(len(indexes) - 1):
                fragments.append(self.fragmentize(indexes[i], indexes[i + 1]))
            return tuple(fragments)
        else:
            return self.fragmentize(0, None),

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def release_date(self) -> t.Optional[datetime.date]:
        return self._release_date

    @property
    def booster_key(self) -> t.Optional[BoosterKey]:
        return self._booster_key

    @property
    def booster_expansion_collection(self) -> t.Optional[ExpansionCollection]:
        return self._booster_expansion_collection

    @property
    def border(self) -> t.Optional[Border]:
        return self._border

    @property
    def magic_card_info_code(self) -> t.Optional[str]:
        return self._magic_card_info_code

    @property
    def mkm_name(self) -> t.Optional[str]:
        return self._mkm_name

    @property
    def mkm_id(self) -> t.Optional[int]:
        return self._mkm_id


class ExpansionFragment(_ExpansionFragment):
    primary_key = PrimaryKey(('of', 'frm', 'to'))

    def __init__(self, of: _Expansion, frm: t.Union[int, None], to: t.Union[int, None]):
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
    def block(self) -> Block:
        return self._of.block

    @property
    def printings(self) -> t.AbstractSet[Printing]:
        return self._printings

    def fragmentize(self, frm: t.Optional[int] = 0, to: t.Optional[int] = None) -> ExpansionFragment:
        return ExpansionFragment(self, to, frm)

    def generate_booster(self) -> 'Booster':
        pass

    @property
    def fragments(self) -> t.Tuple[ExpansionFragment, ...]:
        return self._of.fragments

    @property
    def name(self) -> str:
        return self._of.name

    @property
    def code(self) -> str:
        return self._of.code

    @property
    def release_date(self) -> t.Optional[datetime.date]:
        return self._of.release_date

    @property
    def booster_key(self) -> t.Optional[BoosterKey]:
        return self._of.booster_key

    @property
    def booster_expansion_collection(self) -> t.Optional[ExpansionCollection]:
        return self._of.booster_expansion_collection

    @property
    def border(self) -> t.Optional[Border]:
        return self._of.border

    @property
    def magic_card_info_code(self) -> t.Optional[str]:
        return self._of.magic_card_info_code

    @property
    def mkm_name(self) -> t.Optional[str]:
        return self._of.mkm_name

    @property
    def mkm_id(self) -> t.Optional[int]:
        return self._of.mkm_id
