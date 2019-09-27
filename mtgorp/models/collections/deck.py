import typing as t

from yeetlong.multiset import FrozenMultiset

from mtgorp.models.persistent.printing import Printing
from mtgorp.tools.search.pattern import Criteria, PrintingPatternBuilder
from mtgorp.models.persistent.attributes import typeline
from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator


class Deck(Serializeable):

    def __init__(self, maindeck: t.Iterable[Printing], sideboard: t.Iterable[Printing] = None):
        self._maindeck: FrozenMultiset[Printing] = (
            maindeck
            if isinstance(maindeck, FrozenMultiset)
            else FrozenMultiset(maindeck)
        )

        self._sideboard: FrozenMultiset[Printing] = (
            (
                sideboard
                if isinstance(sideboard, FrozenMultiset) else
                FrozenMultiset(sideboard)
            )
            if sideboard is not None else
            FrozenMultiset()
        )

    @property
    def maindeck(self) -> FrozenMultiset[Printing]:
        return self._maindeck

    @property
    def sideboard(self) -> FrozenMultiset[Printing]:
        return self._sideboard

    @property
    def seventy_five(self) -> FrozenMultiset[Printing]:
        return self._maindeck + self._sideboard

    def __iter__(self) -> t.Iterable[Printing]:
        return self.seventy_five.__iter__()

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Deck)
            and self._maindeck == other.maindeck
            and self._sideboard == other.sideboard
        )

    def __hash__(self) -> int:
        return hash(self.seventy_five)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({len(self._maindeck)}, {len(self._sideboard)})'

    def serialize(self) -> serialization_model:
        return {
            'maindeck': list(self._maindeck),
            'sideboard': list(self._sideboard),
        }

    @classmethod
    def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Deck':
        return Deck(
            inflator.inflate_all(Printing, value['maindeck']),
            inflator.inflate_all(Printing, value.get('sideboard', ())),
        )

# @classmethod
# def deserialize(cls, tree: serialization_model) -> 'Deck':
# 	return Deck(
# 		tree['maindeck'],
# 		tree.get('sideboard', None),
# 	)

# @classmethod
# def _groupify(
# 	cls,
# 	printings: t.Iterable[Printing],
# 	patterns: t.Iterable[Criteria],
# ) -> t.List[Multiset[Printing]]:
#
# 	_printings = list(printings)
# 	out = []
#
# 	for pattern in patterns:
# 		matches = Multiset()
# 		i = 0
# 		while i <len(_printings):
# 			if pattern.match(_printings[i]):
# 				matches.add(_printings.pop(i))
# 			else:
# 				i += 1
# 		out.append(matches)
#
# 	out.append(Multiset(_printings))
#
# 	return out
#
# _CREATURE = PrintingPatternBuilder().type_line.contains(typeline.CREATURE).all()
# _NON_CREATURE_NON_LAND = (
# 	PrintingPatternBuilder()
# 		.type_line
# 		.contains
# 		.no(typeline.CREATURE)
# 		.type_line
# 		.contains
# 		.no(typeline.LAND)
# 		.all()
# )
#
# @classmethod
# def named_list(cls, printings: Multiset[Printing]) -> str:
# 	return '\n'.join(
# 		f'{multiplicity}x [{printing.expansion.code}] {printing.cardboard.name}'
# 		for printing, multiplicity in
# 		printings.items()
# 	)
#
# def to_list(self) -> str:
# 	return '\n\n'.join(
# 		self.named_list(group)
# 		for group in
# 		self._groupify(
# 			self.maindeck,
# 			(
# 				self._CREATURE,
# 				self._NON_CREATURE_NON_LAND,
# 			)
# 		)
# 	)