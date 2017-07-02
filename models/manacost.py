from models import colors as c
import typing as t
import copy
import re
import multiset

class ManaCostAtom(object):
	def __init__(self, code: str, associations: t.FrozenSet[c.Color]=None, cmc_value: int=1):
		self.code = code
		self.associations = associations if associations is not None else frozenset()
		self.cmc_value = cmc_value
	def __repr__(self):
		return '{{{}}}'.format(self.code)
	def __eq__(self, other):
		return isinstance(other, ManaCostAtom) and self.code == other.code
	def __hash__(self):
		return hash(self.code)

def _color_sorted(singulars: t.Iterable[ManaCostAtom]):
	return sorted(
		singulars,
		key=lambda atom: sum(c.COLORS[color] for color in atom.associations)
	)

class GenericCostAtom(ManaCostAtom):
	def __init__(self, amount):
		super(GenericCostAtom, self).__init__(str(amount), cmc_value=amount)
		self.amount = amount
	def __eq__(self, other):
		return isinstance(other, GenericCostAtom) and self.amount == other.amount
	def __hash__(self):
		return hash(self.amount)

class HybridCostAtom(ManaCostAtom):
	def __init__(self, options: t.Iterable[ManaCostAtom]):
		self.options = options if isinstance(options, frozenset) else frozenset(options)
		super(HybridCostAtom, self).__init__(
			code='/'.join(
				option.code
				for option in (
					HybridCostAtom._flatten_options(
						_color_sorted(
							self.options
						)
					)
				)
			),
			associations=frozenset(
				frozenset.union(*[option.associations for option in self.options])
			),
			cmc_value=max(option.cmc_value for option in self.options)
		)
	@classmethod
	def _flatten_options(cls, items: t.Iterable[ManaCostAtom]):
		for item in items:
			if isinstance(item, cls):
				for sub_item in HybridCostAtom._flatten_options(item.options):
					yield sub_item
			else:
				yield item
	def __eq__(self, other):
		return isinstance(other, HybridCostAtom) and self.options == other.options
	def __hash__(self):
		return hash(self.options)

class PhyrexianCostAtom(ManaCostAtom):
	pass

ONE_WHITE = ManaCostAtom('W', frozenset({c.WHITE}))
ONE_BLUE = ManaCostAtom('U', frozenset({c.BLUE}))
ONE_BLACK = ManaCostAtom('B', frozenset({c.BLACK}))
ONE_RED = ManaCostAtom('R', frozenset({c.RED}))
ONE_GREEN = ManaCostAtom('G', frozenset({c.GREEN}))

ONE_PHYREXIAN_WHITE = PhyrexianCostAtom('WP', frozenset({c.WHITE}))
ONE_PHYREXIAN_BLUE = PhyrexianCostAtom('UP', frozenset({c.BLUE}))
ONE_PHYREXIAN_BLACK = PhyrexianCostAtom('BP', frozenset({c.BLACK}))
ONE_PHYREXIAN_RED = PhyrexianCostAtom('RP', frozenset({c.RED}))
ONE_PHYREXIAN_GREEN = PhyrexianCostAtom('GP', frozenset({c.GREEN}))

ONE_COLORLESS = ManaCostAtom('C')
VARIABLE_GENERIC = ManaCostAtom('X', cmc_value=0)
ONE_SNOW = ManaCostAtom('S')

SINGULAR_ATOM_MAP = {
	singular.code: singular for singular in (
		ONE_WHITE,
		ONE_BLUE,
		ONE_BLACK,
		ONE_RED,
		ONE_GREEN,
		ONE_PHYREXIAN_WHITE,
		ONE_PHYREXIAN_BLUE,
		ONE_PHYREXIAN_BLACK,
		ONE_PHYREXIAN_RED,
		ONE_PHYREXIAN_GREEN,
		ONE_COLORLESS,
		VARIABLE_GENERIC,
		ONE_SNOW
	)
}

ZERO_GENERIC = GenericCostAtom(0)
ONE_GENERIC = GenericCostAtom(1)
TWO_GENERIC = GenericCostAtom(2)
THREE_GENERIC = GenericCostAtom(3)
FOUR_GENERIC = GenericCostAtom(4)
FIVE_GENERIC = GenericCostAtom(5)
SIX_GENERIC = GenericCostAtom(6)
SEVEN_GENERIC= GenericCostAtom(7)
EIGHT_GENERIC = GenericCostAtom(8)
NINE_GENERIC = GenericCostAtom(9)
TEN_GENERIC = GenericCostAtom(10)
ELEVEN_GENERIC = GenericCostAtom(11)
TWELVE_GENERIC = GenericCostAtom(12)
THIRTEEN_GENERIC = GenericCostAtom(13)
FOURTEEN_GENERIC = GenericCostAtom(14)
FIFTEEN_GENERIC = GenericCostAtom(15)
SIXTEEN_GENERIC = GenericCostAtom(16)

GENERIC_WHITE = HybridCostAtom({ONE_WHITE, TWO_GENERIC})
GENERIC_BLUE = HybridCostAtom({ONE_BLUE, TWO_GENERIC})
GENERIC_BLACK = HybridCostAtom({ONE_BLACK, TWO_GENERIC})
GENERIC_RED = HybridCostAtom({ONE_RED, TWO_GENERIC})
GENERIC_GREEN = HybridCostAtom({ONE_GREEN, TWO_GENERIC})

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

class ManaCost(object):
	def __init__(self, atoms: t.Iterable[ManaCostAtom]):
		self.atoms = atoms if isinstance(atoms, multiset.FrozenMultiset) else multiset.FrozenMultiset(atoms)
	@property
	def sorted_atoms(self) -> t.List[ManaCostAtom]:
		atoms = list(self.atoms)
		sorted_atoms = []
		for atom in copy.copy(atoms):
			if atom == VARIABLE_GENERIC:
				atoms.remove(atom)
				sorted_atoms.append(atom)
		for atom in copy.copy(atoms):
			if isinstance(atom, GenericCostAtom):
				atoms.remove(atom)
				sorted_atoms.append(atom)
		for atom in copy.copy(atoms):
			if atom == ONE_COLORLESS:
				atoms.remove(atom)
				sorted_atoms.append(atom)
		for atom in _color_sorted(
			list(atom for atom in atoms if isinstance(atom, HybridCostAtom))
		):
			atoms.remove(atom)
			sorted_atoms.append(atom)
		for color in c.COMBINATIONS.get(
			frozenset((col for atom in atoms if isinstance(atom, PhyrexianCostAtom) for col in atom.associations)), ()
		):
			for atom in tuple(item for item in atoms if isinstance(item, PhyrexianCostAtom)):
				if color in atom.associations:
					atoms.remove(atom)
					sorted_atoms.append(atom)
		for color in c.COMBINATIONS.get(frozenset((col for atom in atoms for col in atom.associations)), ()):
			for atom in copy.copy(atoms):
				if color in atom.associations:
					atoms.remove(atom)
					sorted_atoms.append(atom)
		sorted_atoms.extend(atoms)
		return sorted_atoms
	@property
	def cmc(self) -> int:
		return sum(atom.cmc_value for atom in self.atoms)
	@property
	def colors(self) -> t.FrozenSet[c.Color]:
		return frozenset(set.union(*(set(atom.associations) for atom in self.atoms)))
	def __eq__(self, other):
		return isinstance(other, ManaCost) and self.atoms == other.atoms
	def __hash__(self):
		return hash(self.atoms)
	def __str__(self):
		return ''.join(str(atom) for atom in self.sorted_atoms)
	def __iter__(self):
		return self.atoms.__iter__()


class ManaCostParseException(Exception): pass

class Parser(object):
	generic_matcher = re.compile('\\d+$')
	singular_matcher = re.compile('\\w+$')
	matcher = re.compile('[^\\s/]+')
	atom_matcher = re.compile('{([^\\s{}]+)}')
	@staticmethod
	def parse_singular_atom(s: str) -> ManaCostAtom:
		if Parser.generic_matcher.match(s):
			return GenericCostAtom(int(s))
		if Parser.singular_matcher.match(s):
			try:
				return SINGULAR_ATOM_MAP[s]
			except KeyError:
				pass
		raise ManaCostParseException()
	@staticmethod
	def parse_atom(s: str) -> ManaCostAtom:
		singulars = tuple(Parser.parse_singular_atom(m.group()) for m in Parser.matcher.finditer(s))
		if len(singulars) == 1:
			return singulars[0]
		if len(singulars) > 1:
			return HybridCostAtom(singulars)
		raise ManaCostParseException
	@staticmethod
	def parse_string(s: str) -> ManaCost:
		return ManaCost(tuple(Parser.parse_atom(m.group(1)) for m in Parser.atom_matcher.finditer(s)))


def test():
	print(WR_HYBRID)

if __name__ == '__main__':
	test()