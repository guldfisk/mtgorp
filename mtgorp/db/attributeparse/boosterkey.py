import typing as t

from mtgorp.db.attributeparse import parser
from mtgorp.models.limited import constants, boostergen
from mtgorp.models.persistent.attributes import typeline
from mtgorp.tools.search.pattern import CriteriaBuilder


class Parser(parser.Parser):
    CARD_WITH_MYTHIC = constants.KeySlot(
        {
            constants.MYTHIC: 1,
            constants.RARE: 7,
            constants.UNCOMMON: 21,
            constants.COMMON: 77,
        }
    )
    CARD = constants.KeySlot(
        {
            constants.RARE: 1,
            constants.UNCOMMON: 3,
            constants.COMMON: 11,
        }
    )

    SLOT_MAP: t.Dict[t.Union[t.AbstractSet[str], str], constants.KeySlot] = {
        'double faced mythic rare': constants.KeySlot((constants.DOUBLEFACED_MYTHIC,)),
        'double faced uncommon': constants.KeySlot((constants.DOUBLEFACED_UNCOMMON,)),
        'foil uncommon': constants.UNCOMMON_SLOT,
        'double faced common': constants.KeySlot((constants.DOUBLEFACED_COMMON,)),
        'common': constants.COMMON_SLOT,
        'double faced rare': constants.KeySlot((constants.DOUBLEFACED_RARE,)),
        'double faced': constants.KeySlot({
            constants.DOUBLEFACED_MYTHIC: 1,
            constants.DOUBLEFACED_RARE: 7,
            constants.DOUBLEFACED_UNCOMMON: 21,
            constants.DOUBLEFACED_COMMON: 77,
        }),
        'foil rare': constants.RARE_SLOT,
        'draft-matters': constants.KeySlot({
            constants.DRAFT_MATTERS_MYTHIC: 1,
            constants.DRAFT_MATTERS_RARE: 7,
            constants.DRAFT_MATTERS_UNCOMMON: 21,
            constants.DRAFT_MATTERS_COMMON: 77,
        }),
        'foil mythic rare': constants.MYTHIC_SLOT,
        'rare': constants.RARE_SLOT,
        'land': constants.BASIC_SLOT,
        'timeshifted uncommon': constants.KeySlot((constants.TIMESHIFTED_UNCOMMON,)),
        'uncommon': constants.UNCOMMON_SLOT,
        'timeshifted common': constants.KeySlot((constants.TIMESHIFTED_COMMON,)),
        'urza land': constants.KeySlot((
            constants.Option(
                CriteriaBuilder().type_line.contains(typeline.URZAS).all(),
            ),
        )),
        'timeshifted rare': constants.KeySlot((constants.TIMESHIFTED_RARE,)),
        'power nine': constants.PREMIUM_SLOT,
        'mythic rare': constants.MYTHIC_SLOT,
        'foil common': constants.COMMON_SLOT,
        'timeshifted purple': constants.KeySlot({
            constants.TIMESHIFTED_RARE: 1,
            constants.TIMESHIFTED_UNCOMMON: 3,
            constants.TIMESHIFTED_COMMON: 11,
        }),
        frozenset(('land', 'checklist')): constants.BASIC_SLOT,
        frozenset(('rare', 'timeshifted rare')): constants.KeySlot({
            constants.TIMESHIFTED_RARE: 1,
            constants.RARE: 7,
        }),
        frozenset(('rare', 'uncommon')): constants.KeySlot({
            constants.RARE: 1,
            constants.UNCOMMON: 3,
        }),
        frozenset(('foil mythic rare', 'foil rare', 'foil uncommon', 'foil common')): CARD_WITH_MYTHIC,
        'foil_with_mythic': CARD_WITH_MYTHIC,
        'foil': CARD,
        frozenset(('power nine', 'foil')): constants.KeySlot({
            constants.SPECIAL: 1,
            constants.MYTHIC: 53,
            constants.RARE: 371,
            constants.UNCOMMON: 1113,
            constants.COMMON: 4081,
        }),
        frozenset(('common', ('double faced rare', 'double faced mythic rare'))): constants.KeySlot({
            constants.DOUBLEFACED_MYTHIC: 1,
            constants.DOUBLEFACED_RARE: 7,
            constants.COMMON: 49,
        }),
        frozenset(('uncommon', 'timeshifted uncommon')): constants.UNCOMMON_SLOT,
        frozenset(('common', 'timeshifted common')): constants.COMMON_SLOT,
        frozenset(('timeshifted rare', 'timeshifted uncommon')): constants.RARE_SLOT,
        frozenset(('common', 'double faced rare', 'double faced mythic rare')): constants.KeySlot({
            constants.DOUBLEFACED_MYTHIC: 1,
            constants.DOUBLEFACED_RARE: 7,
            constants.COMMON: 49,
        }),
        frozenset(('double faced common', 'double faced uncommon')): constants.KeySlot({
            constants.UNCOMMON: 3,
            constants.COMMON: 11,
        }),
        frozenset(('rare', 'mythic rare')): constants.RARE_MYTHIC_SLOT,
        frozenset(('common', 'premium')): constants.KeySlot({
            constants.PREMIUM: 1,
            constants.COMMON: 143,
        })
    }

    @classmethod
    def _frozen_flatten(cls, value: t.Any) -> t.Union[str, t.AbstractSet]:
        return value if isinstance(value, str) else frozenset(map(cls._frozen_flatten, value))

    @classmethod
    def parse(cls, values: t.Iterable[t.Union[str, t.Tuple[str, ...]]]) -> boostergen.BoosterKey:
        return boostergen.BoosterKey(
            Parser.SLOT_MAP[key]
            for key in
            map(cls._frozen_flatten, values)
            if key in Parser.SLOT_MAP
        )
