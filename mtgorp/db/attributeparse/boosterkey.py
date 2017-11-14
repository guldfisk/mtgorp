import typing as t

from mtgorp.db.attributeparse import parser
from mtgorp.models.limited import boostergen
from mtgorp.models.persistent.attributes import cardtypes
from mtgorp.tools.search.pattern import PrintingPatternBuilder

class Parser(parser.Parser):
	CARD_WITH_MYTHIC = boostergen.KeySlot({
		boostergen.MYTHIC: 1,
		boostergen.RARE: 7,
		boostergen.UNCOMMON: 21,
		boostergen.COMMON: 77,
	})
	CARD = boostergen.KeySlot({
		boostergen.RARE: 1,
		boostergen.UNCOMMON: 3,
		boostergen.COMMON: 11,
	})
	SLOT_MAP = {
		'double faced mythic rare': boostergen.KeySlot((boostergen.DOUBLEFACED_MYTHIC,)),
		'double faced uncommon': boostergen.KeySlot((boostergen.DOUBLEFACED_UNCOMMON,)),
		'foil uncommon': boostergen.UNCOMMON_SLOT,
		'double faced common': boostergen.KeySlot((boostergen.DOUBLEFACED_COMMON,)),
		'common': boostergen.COMMON_SLOT,
		'double faced rare': boostergen.KeySlot((boostergen.DOUBLEFACED_RARE,)),
		'foil rare': boostergen.RARE_SLOT,
		'draft-matters': boostergen.KeySlot({
			boostergen.DRAFT_MATTERS_mythic: 1,
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
				'urzas_land',
				PrintingPatternBuilder().types.contains(cardtypes.CardSubType("Urza's")).build(),
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
		('land', 'checklist'): boostergen.BASIC_SLOT,
		('rare', 'timeshifted rare'): boostergen.KeySlot({
			boostergen.TIMESHIFTED_RARE: 1,
			boostergen.RARE: 7,
		}),
		('rare', 'uncommon'): boostergen.KeySlot({
			boostergen.RARE: 1,
			boostergen.UNCOMMON_SLOT: 3,
		}),
		('foil mythic rare', 'foil rare', 'foil uncommon', 'foil common'): CARD_WITH_MYTHIC,
		'foil_with_mythic': CARD_WITH_MYTHIC,
		'foil': CARD,
		('power nine', 'foil'):  boostergen.KeySlot({
			boostergen.SPECIAL: 1,
			boostergen.MYTHIC: 53,
			boostergen.RARE: 371,
			boostergen.UNCOMMON: 1113,
			boostergen.COMMON: 4081,
		}),
		('common', ('double faced rare', 'double faced mythic rare')): boostergen.KeySlot({
			boostergen.DOUBLEFACED_MYTHIC: 1,
			boostergen.DOUBLEFACED_RARE: 7,
			boostergen.COMMON: 49,
		}),
		('uncommon', 'timeshifted uncommon'): boostergen.UNCOMMON_SLOT,
		('common', 'timeshifted common'): boostergen.COMMON_SLOT,
		('timeshifted rare', 'timeshifted uncommon'): boostergen.RARE_SLOT,
		('common', 'double faced rare', 'double faced mythic rare'): boostergen.KeySlot({
			boostergen.DOUBLEFACED_MYTHIC: 1,
			boostergen.DOUBLEFACED_RARE: 7,
			boostergen.COMMON: 49,
		}),
		('double faced common', 'double faced uncommon'): boostergen.KeySlot({
			boostergen.UNCOMMON: 3,
			boostergen.COMMON: 11,
		}),
		('rare', 'mythic rare'): boostergen.RARE_MYTHIC_SLOT,
		('common', 'premium'): boostergen.KeySlot({
			boostergen.PREMIUM: 1,
			boostergen.COMMON: 143,
		})
	}
	@staticmethod
	def parse(values: t.Tuple[t.Union[str, t.Tuple[str, ...]], ...]) -> boostergen.BoosterKey:
		return boostergen.BoosterKey(
			Parser.SLOT_MAP[key]
			for key in
			(value if isinstance(value, str) else tuple(value) for value in values)
			if key in Parser.SLOT_MAP
		)