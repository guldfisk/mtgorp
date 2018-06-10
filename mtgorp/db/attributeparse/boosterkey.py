import typing as t

from mtgorp.db.attributeparse import parser
from mtgorp.models.limited import boostergen
from mtgorp.models.persistent.attributes import typeline
from mtgorp.tools.search.pattern import PrintingPatternBuilder


class Parser(parser.Parser):
	CARD_WITH_MYTHIC = boostergen.KeySlot(
		{
			boostergen.MYTHIC: 1,
			boostergen.RARE: 7,
			boostergen.UNCOMMON: 21,
			boostergen.COMMON: 77,
		}
	)
	CARD = boostergen.KeySlot(
		{
			boostergen.RARE: 1,
			boostergen.UNCOMMON: 3,
			boostergen.COMMON: 11,
		}
	)

	SLOT_MAP = {
		'double faced mythic rare': boostergen.KeySlot((boostergen.DOUBLEFACED_MYTHIC,)),
		'double faced uncommon': boostergen.KeySlot((boostergen.DOUBLEFACED_UNCOMMON,)),
		'foil uncommon': boostergen.UNCOMMON_SLOT,
		'double faced common': boostergen.KeySlot((boostergen.DOUBLEFACED_COMMON,)),
		'common': boostergen.COMMON_SLOT,
		'double faced rare': boostergen.KeySlot((boostergen.DOUBLEFACED_RARE,)),
		'foil rare': boostergen.RARE_SLOT,
		'draft-matters': boostergen.KeySlot({
			boostergen.DRAFT_MATTERS_MYTHIC: 1,
			boostergen.DRAFT_MATTERS_RARE: 7,
			boostergen.DRAFT_MATTERS_UNCOMMON: 21,
			boostergen.DRAFT_MATTERS_COMMON: 77,
		}),
		'foil mythic rare': boostergen.MYTHIC_SLOT,
		'rare': boostergen.RARE_SLOT,
		'land': boostergen.BASIC_SLOT,
		'timeshifted uncommon': boostergen.KeySlot((boostergen.TIMESHIFTED_UNCOMMON,)),
		'uncommon': boostergen.UNCOMMON_SLOT,
		'timeshifted common': boostergen.KeySlot((boostergen.TIMESHIFTED_COMMON,)),
		'urza land': boostergen.KeySlot((
			boostergen.Option(
				PrintingPatternBuilder().type_line.contains(typeline.URZAS).all(),
			),
		)),
		'timeshifted rare': boostergen.KeySlot((boostergen.TIMESHIFTED_RARE,)),
		'power nine': boostergen.PREMIUM_SLOT,
		'mythic rare': boostergen.MYTHIC_SLOT,
		'foil common': boostergen.COMMON_SLOT,
		'timeshifted purple': boostergen.KeySlot({
			boostergen.TIMESHIFTED_RARE: 1,
			boostergen.TIMESHIFTED_UNCOMMON: 3,
			boostergen.TIMESHIFTED_COMMON: 11,
		}),
		frozenset(('land', 'checklist')): boostergen.BASIC_SLOT,
		frozenset(('rare', 'timeshifted rare')): boostergen.KeySlot({
			boostergen.TIMESHIFTED_RARE: 1,
			boostergen.RARE: 7,
		}),
		frozenset(('rare', 'uncommon')): boostergen.KeySlot({
			boostergen.RARE: 1,
			boostergen.UNCOMMON_SLOT: 3,
		}),
		frozenset(('foil mythic rare', 'foil rare', 'foil uncommon', 'foil common')): CARD_WITH_MYTHIC,
		'foil_with_mythic': CARD_WITH_MYTHIC,
		'foil': CARD,
		frozenset(('power nine', 'foil')):  boostergen.KeySlot({
			boostergen.SPECIAL: 1,
			boostergen.MYTHIC: 53,
			boostergen.RARE: 371,
			boostergen.UNCOMMON: 1113,
			boostergen.COMMON: 4081,
		}),
		frozenset(('common', ('double faced rare', 'double faced mythic rare'))): boostergen.KeySlot({
			boostergen.DOUBLEFACED_MYTHIC: 1,
			boostergen.DOUBLEFACED_RARE: 7,
			boostergen.COMMON: 49,
		}),
		frozenset(('uncommon', 'timeshifted uncommon')): boostergen.UNCOMMON_SLOT,
		frozenset(('common', 'timeshifted common')): boostergen.COMMON_SLOT,
		frozenset(('timeshifted rare', 'timeshifted uncommon')): boostergen.RARE_SLOT,
		frozenset(('common', 'double faced rare', 'double faced mythic rare')): boostergen.KeySlot({
			boostergen.DOUBLEFACED_MYTHIC: 1,
			boostergen.DOUBLEFACED_RARE: 7,
			boostergen.COMMON: 49,
		}),
		frozenset(('double faced common', 'double faced uncommon')): boostergen.KeySlot({
			boostergen.UNCOMMON: 3,
			boostergen.COMMON: 11,
		}),
		frozenset(('rare', 'mythic rare')): boostergen.RARE_MYTHIC_SLOT,
		frozenset(('common', 'premium')): boostergen.KeySlot({
			boostergen.PREMIUM: 1,
			boostergen.COMMON: 143,
		})
	} #type: t.Dict[t.Union[t.AbstractSet[str], str], boostergen.KeySlot]

	@staticmethod
	def parse(values: t.Tuple[t.Union[str, t.Tuple[str, ...]], ...]) -> boostergen.BoosterKey:
		return boostergen.BoosterKey(
			Parser.SLOT_MAP[key]
			for key in
			(value if isinstance(value, str) else frozenset(value) for value in values)
			if key in Parser.SLOT_MAP
		)