import typing as t

from multiset import Multiset

from mtgorp.models.persistent import printing as _printing
from mtgorp.models.persistent import expansion as _expansion


class Booster(object):

	def __init__(self, printings: 't.Iterable[_printing.Printing]', expansion: '_expansion.Expansion' = None):
		self._printings = printings if isinstance(printings, Multiset) else Multiset(printings)
		self._expansion = expansion

	@property
	def printings(self) -> 't.Set[_printing.Printing]':
		return self._printings

	@property
	def sorted_printings(self) -> 't.List[_printing.Printing]':
		return sorted(self._printings, key=lambda p: p.rarity.value, reverse=True)

	@property
	def expansion(self):
		return self._expansion

	def __str__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			tuple(a_printing.cardboard.name for a_printing in self.sorted_printings),
		)

	def __contains__(self, printing: '_printing.Printing') -> bool:
		return printing in self._printings

	def __iter__(self):
		return self._printings.__iter__()


def test():
	from mtgorp.db.load import Loader
	db = Loader.load()
	
	cb1 = db.cardboards['Fire // Ice']
	cb2 = db.cardboards['Lightning Bolt']
	cb3 = db.cardboards['Boneyard Parley']
	cb4 = db.cardboards["River Heralds' Boon"]

	cbs = (cb1, cb2, cb3, cb4)

	ps = (cb.printing for cb in cbs)

	booster = Booster(ps)

	print(booster)
	
if __name__ == '__main__':
	test()