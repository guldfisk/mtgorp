import itertools
import bisect
import random
import typing as t

from multiset import Multiset, BaseMultiset

from mtgorp.models.persistent import expansion as _expansion
from mtgorp.models.persistent import printing as _printing
from mtgorp.tools.search.pattern import PrintingPatternBuilder, Pattern
from mtgorp.models.limited import booster as _booster
from mtgorp.utilities.containers import HashableMultiset
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flag
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes import cardtypes

random.seed()

def sample_multiset(ms: BaseMultiset):
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

class ExpansionCollection(object):
	def __init__(
		self,
		main: '_expansion.Expansion',
		basics: '_expansion.Expansion' = None,
		premium: '_expansion.Expansion' = None,
		**expansions: '_expansion.Expansion'
	):
		self._expansions = {
			'main': main,
			'basics': basics,
			'premium': premium,
		}
		self._expansions.update(expansions)
	def __getitem__(self, item: str) -> '_expansion.Expansion':
		return self._expansions[item]
	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			self._expansions,
		)

class Option(object):
	def __init__(self, name: str, pattern: Pattern, collection_key: str = 'main'):
		self._name = name
		self._pattern = pattern
		self._collection_key = collection_key
	@property
	def name(self):
		return self._name
	@property
	def pattern(self):
		return self._pattern
	@property
	def collection_key(self):
		return self._collection_key
	def __hash__(self):
		return hash((self.__class__, self._name))
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._name == other.name
	# def __repr__(self):
	# 	return '{}({})'.format(
	# 		self.__class__.__name__,
	# 		self._name,
	# 	)

COMMON = Option('common', PrintingPatternBuilder().rarity.equals(Rarity.COMMON).build())
UNCOMMON = Option('uncommon', PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).build())
RARE = Option('rare', PrintingPatternBuilder().rarity.equals(Rarity.RARE).build())
MYTHIC = Option('mythic', PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).build())
SPECIAL = Option('special', PrintingPatternBuilder().rarity.equals(Rarity.SPECIAL).build())
TIMESHIFTED_COMMON = Option(
	'timeshifted_common',
	PrintingPatternBuilder().rarity.equals(Rarity.COMMON).flags.contains(Flag.TIMESHIFTED).build(),
)
TIMESHIFTED_UNCOMMON = Option(
	'timeshifted_uncommon',
	PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).flags.contains(Flag.TIMESHIFTED).build(),
)
TIMESHIFTED_RARE = Option(
	'timeshifted_rare',
	PrintingPatternBuilder().rarity.equals(Rarity.RARE).flags.contains(Flag.TIMESHIFTED).build(),
)
TIMESHIFTED_MYTHIC = Option(
	'timeshifted_mythic',
	PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).flags.contains(Flag.TIMESHIFTED).build(),
)
DOUBLEFACED_COMMON = Option(
	'timeshifted_common',
	PrintingPatternBuilder().rarity.equals(Rarity.COMMON).layout.equals(Layout.TRANSFORM).build(),
)
DOUBLEFACED_UNCOMMON = Option(
	'timeshifted_uncommon',
	PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).layout.equals(Layout.TRANSFORM).build(),
)
DOUBLEFACED_RARE = Option(
	'timeshifted_rare',
	PrintingPatternBuilder().rarity.equals(Rarity.RARE).layout.equals(Layout.TRANSFORM).build(),
)
DOUBLEFACED_MYTHIC = Option(
	'timeshifted_mythic',
	PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).layout.equals(Layout.TRANSFORM).build(),
)
PREMIUM = Option(
	'premium',
	PrintingPatternBuilder().build(),
	'premium'
)
BASIC = Option(
	'basic',
	PrintingPatternBuilder().types.contains(cardtypes.BASIC).build(),
	'basics'
)
DRAFT_MATTERS_COMMON = Option(
	'draft_matters_common',
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.COMMON).build(),
)
DRAFT_MATTERS_UNCOMMON = Option(
	'draft_matters_uncommon',
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.UNCOMMON).build(),
)
DRAFT_MATTERS_RARE = Option(
	'draft_matters_rare',
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.RARE).build(),
)
DRAFT_MATTERS_mythic = Option(
	'draft_matters_mythic',
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.MYTHIC).build(),
)

class KeySlot(object):
	def __init__(self, options: t.Iterable[Option]):
		self._options = options if isinstance(options, HashableMultiset) else HashableMultiset(options)
	def get_map_slot(self, expansion_collection: ExpansionCollection) -> 'MapSlot':
		return MapSlot(
			{
				HashableMultiset(
					printing
					for printing in
					expansion_collection[option.collection_key].printings
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
	# def __repr__(self):
	# 	return '{}({})'.format(
	# 		self.__class__.__name__,
	# 		self._options.items(),
	# 	)

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

class BoosterKey(object):
	def __init__(self, slots: t.Iterable[KeySlot]):
		self._slots = slots if isinstance(slots, HashableMultiset) else HashableMultiset(slots)
	@property
	def slots(self):
		return self._slots
	def get_booster_map(self, expansion_collection: ExpansionCollection) -> 'BoosterMap':
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
	# def __repr__(self):
	# 	return '{}({})'.format(
	# 		self.__class__.__name__,
	# 		self._slots.items(),
	# 	)

class MapSlot(object):
	def __init__(self, options: t.Iterable[HashableMultiset]):
		self.options = options if isinstance(options, HashableMultiset) else HashableMultiset(options)
	def _filter_options(self, forbidden: BaseMultiset):
		for value, multiplicity in self.options.items():
			filtered = value - forbidden
			if filtered:
				yield filtered, multiplicity
	def sample(self, forbidden: BaseMultiset = None):
		if not forbidden:
			return sample_multiset(
				sample_multiset(self.options)
			)
		new_options = Multiset(
			{
				filtered: multiplicity
				for filtered, multiplicity in
				self._filter_options(forbidden)
			}
		)
		if not new_options:
			raise GenerateBoosterException('Ran out of cards')
		return sample_multiset(
			sample_multiset(new_options)
		)
	# def __repr__(self):
	# 	return '{}({})'.format(
	# 		self.__class__.__name__,
	# 		self.options.items(),
	# 	)

class BoosterMap(object):
	def __init__(self, slots: t.Iterable[MapSlot]):
		self.slots = slots if isinstance(slots, HashableMultiset) else HashableMultiset(slots)
	def generate_booster(self) -> _booster.Booster:
		printings = Multiset()
		for slot, multiplicity in self.slots.items():
			forbidden = set()
			for i in range(multiplicity):
				printing = slot.sample(forbidden=forbidden)
				printings.add(printing)
				forbidden.add(printing)
		return _booster.Booster(printings)
	# def __repr__(self):
	# 	return '{}({})'.format(
	# 		self.__class__.__name__,
	# 		self.slots.items(),
	# 	)

def test():
	from mtgorp.db.load import Loader
	from mtgorp.models.persistent.attributes.rarities import Rarity
	db = Loader.load()

	expansion = db.expansions['AKH']

	# another_exp = expansion.Expansion('LOL')
	#
	# another_exp.printings = {db.cardboards[name].printing for name in (
	# 	'Fire // Ice',
	# 	'Fling',
	# 	'Cradle of the Accursed',
	# 	'Vizier of Deferment',
	# 	'Timber Gorge',
	# )}
	#
	# booster_key = BoosterKey(
	# 	{
	# 		COMMON_SLOT: 10,
	# 		UNCOMMON_SLOT: 3,
	# 		RARE_MYTHIC_SLOT: 1,
	# 	}
	# )

	# PrintingPatternBuilder().cmc.less_than_or_equals(2)

	print(expansion._booster_key)

	daze = db.cardboards['Daze'].get_printing(db.expansions['MPS_AKH'])

	expansion.generate_booster()
	print(expansion._booster_map)

	boosters = [expansion.generate_booster() for i in range(1000)]
	print(
		len([booster for booster in boosters if 'MPS_AKH' in [printing.expansion.code for printing in booster]])
	)


if __name__ == '__main__':
	test()