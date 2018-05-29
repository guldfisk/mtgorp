import typing as t

from mtgorp.models.persistent.printing import Printing
from mtgorp.tools.search.pattern import Pattern, PrintingPatternBuilder
from mtgorp.models.persistent.attributes import typeline
from mtgorp.utilities.containers import HashableMultiset, Multiset
from mtgorp.models.collections.serilization.serializeable import Serializeable, model_tree, SerializationException


class Deck(Serializeable):
	
	def __init__(self, maindeck: t.Iterable[Printing], sideboard: t.Iterable[Printing] = None):
		self._maindeck = (
			maindeck
			if isinstance(maindeck, HashableMultiset)
			else HashableMultiset(maindeck)
		) #type: HashableMultiset[Printing]

		self._sideboard = (
			(
				sideboard
				if isinstance(sideboard, HashableMultiset) else
				HashableMultiset(sideboard)
			)
			if sideboard is not None else
			HashableMultiset()
		) #type: HashableMultiset[Printing]
	
	@property
	def maindeck(self) -> HashableMultiset[Printing]:
		return self._maindeck
	
	@property
	def sideboard(self) -> HashableMultiset[Printing]:
		return self._sideboard
	
	@property
	def seventy_five(self) -> HashableMultiset[Printing]:
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

	def to_model_tree(self) -> model_tree:
		return {
			'maindeck': self._maindeck,
			'sideboard': self._sideboard,
		}

	@classmethod
	def from_model_tree(cls, tree: model_tree) -> 'Deck':
		try:
			return Deck(
				tree['maindeck'],
				tree.get('sideboard', None),
			)
		except KeyError:
			raise SerializationException()

	# def to_xml(self) -> str:
	# 	deck = ElementTree.Element('deck')
	# 	maindeck = ElementTree.SubElement(deck, 'maindeck')
	# 	for printing in self._maindeck:
	# 		ElementTree.SubElement(maindeck, str(printing.id))
	# 	sideboard = ElementTree.SubElement(deck, 'sideboard')
	# 	for printing in self._sideboard:
	# 		ElementTree.SubElement(sideboard, str(printing.id))
	# 	return ElementTree.tostring(deck)
	
	@classmethod
	def _groupify(
		cls,
		printings: t.Iterable[Printing],
		patterns: t.Iterable[Pattern],
	) -> t.List[Multiset[Printing]]:

		_printings = list(printings)
		out = []

		for pattern in patterns:
			matches = Multiset()
			i = 0
			while i <len(_printings):
				if pattern.match(_printings[i]):
					matches.add(_printings.pop(i))
				else:
					i += 1
			out.append(matches)

		out.append(Multiset(_printings))

		return out

	_CREATURE = PrintingPatternBuilder().types.contains(typeline.CREATURE).all()
	_NON_CREATURE_NON_LAND = (
		PrintingPatternBuilder()
			.types
			.contains
			.no(typeline.CREATURE)
			.types
			.contains
			.no(typeline.LAND)
			.all()
	)

	@classmethod
	def named_list(cls, printings: Multiset[Printing]) -> str:
		return '\n'.join(
			f'{multiplicity}x [{printing.expansion.code}] {printing.cardboard.name}'
			for printing, multiplicity in
			printings.items()
		)

	def to_list(self) -> str:
		return '\n\n'.join(
			self.named_list(group)
			for group in
			self._groupify(
				self.maindeck,
				(
					self._CREATURE,
					self._NON_CREATURE_NON_LAND,
				)
			)
		)