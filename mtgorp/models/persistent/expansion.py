from __future__ import annotations

import datetime
import typing as t

from orp.models import PrimaryKey, Model
from orp.relationships import Many, One, OneDescriptor

from mtgorp.models.persistent.attributes.expansiontype import ExpansionType
from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.models.interfaces import Block, BoosterKey, ExpansionCollection, Printing, Expansion as _Expansion


class Expansion(Model, _Expansion):
    primary_key = PrimaryKey('code')
    _code: str

    def __init__(
        self,
        code: str,
        name: str = None,
        block: Block = None,
        expansion_type: ExpansionType = None,
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
        self._expansion_type = expansion_type
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

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def expansion_type(self) -> ExpansionType:
        return self._expansion_type

    @property
    def release_date(self) -> t.Optional[datetime.datetime]:
        return self._release_date

    @property
    def booster_key(self) -> t.Optional[BoosterKey]:
        return self._booster_key

    @property
    def booster_expansion_collection(self) -> t.Optional[ExpansionCollection]:
        return self._booster_expansion_collection

    @property
    def fragment_dividers(self) -> t.Sequence[int]:
        return self._fragment_dividers

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
