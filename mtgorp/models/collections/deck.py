import typing as t

import json
from xml.etree import ElementTree

from mtgorp.models.persistent.printing import Printing
from mtgorp.tools.search.pattern import Pattern, PrintingPatternBuilder
from mtgorp.models.persistent.attributes import cardtypes

from mtgorp.utilities.containers import HashableMultiset

class Deck(object):
	def __init__(self, maindeck: t.Iterable[Printing], sideboard: t.Iterable[Printing] = None):
		self._maindeck = maindeck if isinstance(maindeck, HashableMultiset) else HashableMultiset(maindeck)
		self._sideboard = (
			(
				sideboard
				if isinstance(sideboard, HashableMultiset) else
				HashableMultiset(sideboard)
			)
			if sideboard is not None else
			HashableMultiset()
		)
	@property
	def maindeck(self) -> t.FrozenSet[Printing]:
		return self._maindeck
	@property
	def sideboard(self) -> t.FrozenSet[Printing]:
		return self._sideboard
	@property
	def seventy_five(self) -> t.FrozenSet[Printing]:
		return self._maindeck + self._sideboard
	def __iter__(self) -> t.Iterable[Printing]:
		return self.seventy_five.__iter__()
	def __eq__(self, other) -> bool:
		return isinstance(other, Deck) and other.seventy_five == self.seventy_five
	def __hash__(self) -> int:
		return hash(self.seventy_five)
	def to_json(self) -> str:
		return json.dumps(
			{
				'maindeck': tuple(printing.id for printing in self._maindeck),
				'sideboard': tuple(printing.id for printing in self._sideboard),
			}
		)
	def to_xml(self) -> str:
		deck = ElementTree.Element('deck')
		maindeck = ElementTree.SubElement(deck, 'maindeck')
		for printing in self._maindeck:
			ElementTree.SubElement(maindeck, str(printing.id))
		sideboard = ElementTree.SubElement(deck, 'sideboard')
		for printing in self._sideboard:
			ElementTree.SubElement(sideboard, str(printing.id))
		return ElementTree.tostring(deck)
	@staticmethod
	def _groupify(
			printings: t.Iterable[Printing],
			patterns: t.Iterable[Pattern],
	) -> t.List[t.List[Printing]]:
		_printings = list(printings)
		out = []
		for pattern in patterns:
			matches = []
			i = 0
			while i <len(_printings):
				if pattern.match(_printings[i]):
					matches.append(_printings.pop(i))
				else:
					i += 1
			out.append(matches)
		return out
	_CREATURE = PrintingPatternBuilder().types.contains(cardtypes.CREATURE).build()
	_NON_CREATURE = PrintingPatternBuilder().types.contains(cardtypes.CREATURE).build()
	# def to_named_list(self) -> :
	# 	return '\n'.join(
	# 		(self.maindeck.items()
	# 	)