import typing as t
from abc import ABCMeta

import mtgorp.models.persistent.attributes.colors as cols
from mtgorp.models.persistent.attributes.colors import Color as c
from mtgorp.utilities.containers import HashableMultiset


class ManaCostAtom(metaclass=ABCMeta):
	
	def __init__(self, code: str, associations: t.AbstractSet=None, cmc_value: int=1):
		self._code = code
		self._associations = associations if isinstance(associations, frozenset) else frozenset()
		self._cmc_value = cmc_value
	
	@property
	def code(self):
		return self._code
	
	@property
	def associations(self):
		return self._associations
	
	@property
	def cmc_value (self):
		return self._cmc_value
	
	def __repr__(self):
		return '{{{}}}'.format(self.code)
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.code == other.code
	
	def __hash__(self):
		return hash((self.__class__, self.code))
	
	def _lt_tiebreaker(self, other):
		return False
	
	def __lt__(self, other):
		s, o = _atom_sort_value(self), _atom_sort_value(other)
		if s < o:
			return True
		if s == o:
			return self._lt_tiebreaker(other)
		return False


class VariableCostAtom(ManaCostAtom):
	pass


class GenericCostAtom(ManaCostAtom):
	pass


class ColorCostAtom(ManaCostAtom):
	def _lt_tiebreaker(self, other):
		return cols.color_set_sort_value(self.associations) < cols.color_set_sort_value(other.associations)


class ColorlessCostAtom(ManaCostAtom):
	pass


class PhyrexianCostAtom(ManaCostAtom):
	pass


class OtherCostAtom(ManaCostAtom):
	pass


class HybridCostAtom(ManaCostAtom):
	
	def __init__(self, options: 't.AbstractSet[t.Union[ManaCost, ManaCostAtom]]'):
		self._options = frozenset(self._flatten_options(options))
		assert len(self._options) > 1
		super(HybridCostAtom, self).__init__(
			code='/'.join(
				str(option)
				for option in (
					sorted(
						self._options
					)
				)
			),
			associations=frozenset(
				frozenset.union(*[option.colors for option in self._options])
			),
			cmc_value=max(option.cmc for option in self._options)
		)
	
	@property
	def options(self):
		return  self._options
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._options == other.options
	
	def __hash__(self):
		return hash((self.__class__, self._options))
	
	def __iter__(self):
		return self._options.__iter__()
	
	def __len__(self):
		return self._options.__len__()
	
	@staticmethod
	def _flatten_options(mana_costs: 't.AbstractSet[t.Union[ManaCost, ManaCostAtom]]'):
		for option in mana_costs:
			if isinstance(option, ManaCostAtom):
				for mana_cost in HybridCostAtom._flatten_options({ManaCost((option,))}):
					yield mana_cost
			elif len(option)==1 and isinstance(option.__iter__().__next__(), HybridCostAtom):
				for hybrid_mana_cost in HybridCostAtom._flatten_options(option._atoms):
					for sub_mana_cost in hybrid_mana_cost:
						yield sub_mana_cost
			else:
				yield option
	
	def _lt_tiebreaker(self, other):
		s, o = sorted(self._options), sorted(other._options)
		for i in range(min(len(s), len(o))):
			if s[i] < o[i]:
				return True
			if s[i] > o[i]:
				return False
		return len(s) < len(o)


class ManaCost(object):
	
	def __init__(self, atoms: t.Iterable[ManaCostAtom]=None):
		self._atoms = atoms if isinstance(atoms, HashableMultiset) else HashableMultiset(atoms)
	
	@property
	def cmc(self) -> int:
		return sum(atom.cmc_value for atom in self._atoms)
	
	@property
	def colors(self) -> t.FrozenSet[cols.Color]:
		return frozenset(set.union(*(set(atom.associations) for atom in self._atoms)))
	
	def __eq__(self, other):
		return isinstance(other, ManaCost) and self._atoms == other._atoms
	
	def __hash__(self):
		return hash((self.__class__, self._atoms))
	
	def __str__(self):
		if not self._atoms:
			return '{0}'
		accumulated = ''
		generics = 0
		for atom in sorted(self._atoms):
			if atom == ONE_GENERIC:
				generics += 1
				continue
			if generics > 0:
				accumulated += '{{{}}}'.format(generics)
				generics = 0
			accumulated += str(atom)
		if generics > 0:
			accumulated += '{{{}}}'.format(generics)
		return accumulated
	
	def __iter__(self):
		return self._atoms.__iter__()
	
	def __len__(self):
		return self._atoms.__len__()
	
	def __lt__(self, other):
		s, o = sorted(self), sorted(other)
		for i in range(min(len(s), len(o))):
			if s[i] < o[i]:
				return True
			if s[i] > o[i]:
				return False
		return len(s) < len(o)
	
	def __contains__(self, item):
		return item._atoms.issubset(self._atoms)
	
	def __add__(self, other):
		return ManaCost(
			self._atoms + other._atoms
		)
	
	def __sub__(self, other):
		return ManaCost(
			self._atoms.difference(other._atoms)
		)


_cost_type_order = (
	VariableCostAtom,
	GenericCostAtom,
	ColorlessCostAtom,
	HybridCostAtom,
	ColorCostAtom,
	PhyrexianCostAtom,
)

_cost_type_order_map = {
	t: _cost_type_order.index(t) for t in _cost_type_order
}

_MAX_TYPE_ORDER = len(_cost_type_order) + 1


def _atom_sort_value(atom):
	return _cost_type_order_map.get(type(atom), _MAX_TYPE_ORDER)


ONE_WHITE = ColorCostAtom('W', frozenset({c.WHITE}))
ONE_BLUE = ColorCostAtom('U', frozenset({c.BLUE}))
ONE_BLACK = ColorCostAtom('B', frozenset({c.BLACK}))
ONE_RED = ColorCostAtom('R', frozenset({c.RED}))
ONE_GREEN = ColorCostAtom('G', frozenset({c.GREEN}))

ONE_GENERIC = GenericCostAtom('1')

ONE_PHYREXIAN = PhyrexianCostAtom('P')

ONE_PHYREXIAN_WHITE = HybridCostAtom({ONE_WHITE, ONE_PHYREXIAN})
ONE_PHYREXIAN_BLUE = HybridCostAtom({ONE_BLUE, ONE_PHYREXIAN})
ONE_PHYREXIAN_BLACK = HybridCostAtom({ONE_BLACK, ONE_PHYREXIAN})
ONE_PHYREXIAN_RED = HybridCostAtom({ONE_RED, ONE_PHYREXIAN})
ONE_PHYREXIAN_GREEN = HybridCostAtom({ONE_GREEN, ONE_PHYREXIAN})
ONE_PHYREXIAN_GENERIC = HybridCostAtom({ONE_GENERIC, ONE_PHYREXIAN})

ONE_COLORLESS = ColorlessCostAtom('C')
VARIABLE_GENERIC = VariableCostAtom('X', cmc_value=0)
ONE_SNOW = OtherCostAtom('S')

SINGULAR_ATOM_MAP = {
	singular.code: singular for singular in (
		ONE_WHITE,
		ONE_BLUE,
		ONE_BLACK,
		ONE_RED,
		ONE_GREEN,
		ONE_PHYREXIAN,
		ONE_COLORLESS,
		VARIABLE_GENERIC,
		ONE_SNOW,
	)
}

_TWO_GENERIC = ManaCost((ONE_GENERIC, ONE_GENERIC))
GENERIC_WHITE = HybridCostAtom({ONE_WHITE, _TWO_GENERIC})
GENERIC_BLUE = HybridCostAtom({ONE_BLUE, _TWO_GENERIC})
GENERIC_BLACK = HybridCostAtom({ONE_BLACK, _TWO_GENERIC})
GENERIC_RED = HybridCostAtom({ONE_RED, _TWO_GENERIC})
GENERIC_GREEN = HybridCostAtom({ONE_GREEN, _TWO_GENERIC})

WU_HYBRID = HybridCostAtom({ONE_WHITE, ONE_BLUE})
WB_HYBRID = HybridCostAtom({ONE_WHITE, ONE_BLACK})
WR_HYBRID = HybridCostAtom({ONE_WHITE, ONE_RED})
WG_HYBRID = HybridCostAtom({ONE_WHITE, ONE_GREEN})
UB_HYBRID = HybridCostAtom({ONE_BLUE, ONE_BLACK})
UR_HYBRID = HybridCostAtom({ONE_BLUE, ONE_RED})
UG_HYBRID = HybridCostAtom({ONE_BLUE, ONE_GREEN})
BR_HYBRID = HybridCostAtom({ONE_BLACK, ONE_RED})
BG_HYBRID = HybridCostAtom({ONE_BLACK, ONE_GREEN})
RG_HYBRID = HybridCostAtom({ONE_RED, ONE_GREEN})


def test():
	mc1 = ManaCost(
		(
			ONE_BLACK,
			ONE_PHYREXIAN_GREEN,
			ONE_GENERIC,
			ONE_GENERIC,
		)
	)

	mc2= ManaCost(
		(
			ONE_BLACK,
			ONE_PHYREXIAN_GREEN,
			ONE_GENERIC,
			ONE_GENERIC,
			ONE_BLACK,
			VARIABLE_GENERIC,
		),
	)

	mc3 = ManaCost((GENERIC_BLUE,))

	h1 = HybridCostAtom(
		{
			ONE_BLACK,
			ManaCost(
				(
					ONE_GENERIC,
					WU_HYBRID,
				)
			),
		}
	)


if __name__ == '__main__':
	test()