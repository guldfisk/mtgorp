import itertools
import bisect
import random
import typing as t

from multiset import Multiset, BaseMultiset
from frozendict import frozendict

from mtgorp.models.persistent import expansion as _expansion
from mtgorp.models.persistent import printing as _printing
from mtgorp.tools.search.pattern import PrintingPatternBuilder, Pattern
from mtgorp.models.limited import booster as _booster
from mtgorp.utilities.containers import HashableMultiset
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.flags import Flag
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes import cardtypes


def choice_multiset(ms: BaseMultiset):
	values, multiplicities = zip(*ms.items())
	cumulative_distribution = tuple(itertools.accumulate(multiplicities))
	return values[
		bisect.bisect_right(
			cumulative_distribution,
			random.random() * cumulative_distribution[-1]
		)
	]


# def sample_multiset(ms: BaseMultiset, amount: int = 1):
# 	values, multiplicities = zip(*ms.items())
# 	cumulative_distribution = tuple(itertools.accumulate(multiplicities))
# 	return [
# 		values[
# 			bisect.bisect(
# 				cumulative_distribution,
# 				index,
# 			)
# 		] for index in
# 		random.sample(
# 			range(cumulative_distribution[-1]),
# 			amount,
# 		)
# 	 ] #Pretty sure this can select same element twice


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
		self._expansions = frozendict(self._expansions)

	@property
	def main(self):
		return self._expansions['main']

	@property
	def basics(self):
		return self._expansions['basics']

	@property
	def premium(self):
		return self._expansions['premium']

	def __getitem__(self, item: str) -> '_expansion.Expansion':
		return self._expansions[item]

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._expansions == other._expansions

	def __hash__(self):
		return hash((self.__class__, self._expansions))

	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			self._expansions,
		)


class Option(object):

	def __init__(self, pattern: Pattern, collection_key: str = 'main'):
		self._pattern = pattern
		self._collection_key = collection_key

	@property
	def pattern(self):
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


COMMON = Option(PrintingPatternBuilder().rarity.equals(Rarity.COMMON).all())
UNCOMMON = Option(PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).all())
RARE = Option(PrintingPatternBuilder().rarity.equals(Rarity.RARE).all())
MYTHIC = Option(PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).all())
SPECIAL = Option(PrintingPatternBuilder().rarity.equals(Rarity.SPECIAL).all())
TIMESHIFTED_COMMON = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.COMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_UNCOMMON = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_RARE = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.RARE).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_MYTHIC = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).flags.contains(Flag.TIMESHIFTED).all(),
)
DOUBLEFACED_COMMON = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.COMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_UNCOMMON = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.UNCOMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_RARE = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.RARE).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_MYTHIC = Option(
	PrintingPatternBuilder().rarity.equals(Rarity.MYTHIC).layout.equals(Layout.TRANSFORM).all(),
)
PREMIUM = Option(
	PrintingPatternBuilder().all(),
	'premium'
)
BASIC = Option(
	PrintingPatternBuilder().types.contains(cardtypes.BASIC).all(),
	'basics'
)
DRAFT_MATTERS_COMMON = Option(
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.COMMON).all(),
)
DRAFT_MATTERS_UNCOMMON = Option(
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.UNCOMMON).all(),
)
DRAFT_MATTERS_RARE = Option(
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.RARE).all(),
)
DRAFT_MATTERS_MYTHIC = Option(
	PrintingPatternBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.MYTHIC).all(),
)


class KeySlot(object):

	def __init__(self, options: t.Iterable[Option]):
		self._options = options if isinstance(options, HashableMultiset) else HashableMultiset(options)

	def get_map_slot(self, expansion_collection: ExpansionCollection) -> 'MapSlot':
		return MapSlot(
			{
				frozenset(
					printing
					for printing in
					expansion_collection[option.collection_key].printings
					if printing.in_booster and option.pattern.check(printing)
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

	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			self._slots.items(),
		)


class MapSlot(object):

	def __init__(self, options: 't.Iterable[t.FrozenSet[_printing.Printing]]'):
		self.options = options if isinstance(options, HashableMultiset) else HashableMultiset(options)

	# def _filter_options(self, forbidden: BaseMultiset):
	# 	for value, multiplicity in self.options.items():
	# 		filtered = value - forbidden
	# 		if filtered:
	# 			yield filtered, multiplicity

	def sample(self):
		return random.choice(
			choice_multiset(
				self.options
			)
		)

	def sample_slot(self):
		return choice_multiset(self.options)
		# if not forbidden:
		# 	return choice_multiset(
		# 		choice_multiset(self.options)
		# 	)
		# new_options = Multiset(
		# 	{
		# 		filtered: multiplicity
		# 		for filtered, multiplicity in
		# 		self._filter_options(forbidden)
		# 	}
		# )
		# if not new_options:
		# 	raise GenerateBoosterException('Ran out of cards')
		# return choice_multiset(
		# 	choice_multiset(new_options)
		# )


class BoosterMap(object):

	def __init__(self, slots: t.Iterable[MapSlot]):
		self.slots = slots if isinstance(slots, HashableMultiset) else HashableMultiset(slots)

	def generate_booster(self) -> _booster.Booster:
		slots = Multiset(slot.sample_slot() for slot in self.slots)
		printings = Multiset()
		for value, multiplicity in slots.items():
			printings.update(
				random.sample(
					value,
					multiplicity,
				)
			)
		return _booster.Booster(printings)

		# printings = Multiset()
		# for slot, multiplicity in self.slots.items():
		# 	forbidden = set()
		# 	for i in range(multiplicity):
		# 		printing = slot.sample(forbidden=forbidden)
		# 		printings.add(printing)
		# 		forbidden.add(printing)
		# return _booster.Booster(printings)


def test():
	from mtgorp.db.load import Loader
	from mtgorp.models.persistent.attributes.rarities import Rarity
	db = Loader.load()

	expansion = db.expansions['AKH']

	print(expansion._booster_key)

	daze = db.cardboards['Daze'].from_expansion(db.expansions['MPS_AKH'])

	expansion.generate_booster()
	print(expansion._booster_map)

	from mtgorp.utilities.misc import Timer

	timer = Timer()

	boosters = [expansion.generate_booster() for i in range(1000)]

	print('boosters done', timer.middle_time())

	print(boosters[-1])

	print(
		len([booster for booster in boosters if 'MPS_AKH' in [printing.expansion.code for printing in booster]])
	)


if __name__ == '__main__':
	test()