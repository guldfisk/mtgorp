import datetime
import typing as t

from lazy_property import LazyProperty

from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.models.persistent.block import Block
from mtgorp.models.limited import boostergen
from mtgorp.models.limited.booster import Booster
from orp.relationships import Many, One, OneDescriptor
from orp.database import Model, PrimaryKey

class Expansion(Model):
	primary_key = PrimaryKey('code')
	def __init__(
		self,
		code: str,
		name: str = None,
		block: Block = None,
		release_date: datetime.date = None,
		booster_key: 'boostergen.BoosterKey' = None,
		booster_expansion_collection: 'boostergen.ExpansionCollection' = None,
		border: Border = None,
		magic_card_info_code: str = None,
		mkm_name: str = None,
		mkm_id: int = None,
		fragment_dividers: t.Tuple[int, ...] = (),
	):
		self._name = name
		self._block = One(self, 'expansions', block)
		self._release_date = release_date
		self._booster_key = booster_key
		self._booster_expansion_collection = booster_expansion_collection
		self._border = border
		self._magic_card_info_code = magic_card_info_code
		self._mkm_name = mkm_name
		self._mkm_id = mkm_id
		self.printings = Many(self, '_expansion')
		self._fragment_dividers = fragment_dividers
		self._booster_map = None
	block = OneDescriptor('_block')
	def fragmentize(self, frm: t.Union[int, None] = 0, to: t.Union[int, None] = None):
		return ExpansionFragment(self, frm, to)
	def generate_booster(self) -> Booster:
		if self._booster_map is None:
			self._booster_map = self._booster_key.get_booster_map(self._booster_expansion_collection)
		return self._booster_map.generate_booster()
	@LazyProperty
	def fragments(self):
		if self._fragment_dividers:
			fragments = []
			indexes = (0,)+self._fragment_dividers+(None,)
			for i in range(len(indexes)-1):
				fragments.append(self.fragmentize(indexes[i], indexes[i+1]))
			return tuple(fragments)
		else:
			return self.fragmentize(0, None),
	@property
	def name(self) -> str:
		return self._name
	@property
	def code(self) -> str:
		return self._code
	@property
	def release_date(self) -> t.Optional[datetime.date]:
		return self._release_date
	@property
	def booster_key(self) -> 't.Optional[boostergen.BoosterKey]':
		return self._booster_key
	@property
	def booster_expansion_collection(self) -> 't.Optional[boostergen.ExpansionCollection]':
		return self._booster_expansion_collection
	@property
	def border(self) -> t.Optional[Border]:
		return self._border
	@property
	def magic_card_info_code(self) -> t.Optional[str]:
		return self._magic_card_info_code
	@property
	def mkm_name(self) -> t.Optional[str]:
		return self._mkm_name
	@property
	def mkm_id(self) -> t.Optional[int]:
		return self._mkm_id

class ExpansionFragment(Expansion):
	primary_key = PrimaryKey(('of', 'frm', 'to'))
	def __init__(self, of: Expansion, frm: t.Union[int, None], to: t.Union[int, None]):
		for printing in of.printings:
			if printing.collector_number is None:
				print(printing, printing.cardboard.name)
		self.printings = sorted(of.printings, key=lambda printing: printing.collector_number)[frm:to]
	@property
	def of(self):
		return self._of
	@property
	def frm(self):
		return self._frm
	@property
	def to(self):
		return self._to
	def __getattr__(self, item):
		return object.__getattribute__(self, '_of').__getattribute__(item)

def test():
	from mtgorp.db.load import Loader

	db = Loader.load()

	akh = db.expansions['AKH']

	akh_fragment = akh.fragments[0]

	print(akh_fragment, len(akh.printings), len(akh_fragment.printings))

	hou = db.expansions['HOU']

	hou._fragment_dividers = (12, 100)

	print(len(hou.printings))

	for fragment in hou.fragments:
		print(fragment, len(fragment.printings), fragment.code)

if __name__ == '__main__':
	test()