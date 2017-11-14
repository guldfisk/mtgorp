from multiset import FrozenMultiset


class HashableMultiset(FrozenMultiset):
	def __hash__(self):
		return hash(frozenset(self._elements.items()))