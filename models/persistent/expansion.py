import datetime
import typing as t

from models.persistent.attributes.borders import Border
from orp.relationships import Many
from orp.database import Model, PrimaryKey

class Expansion(Model):
	primary_key = PrimaryKey('name')
	def __init__(
		self,
		name: str,
		code: str,
		release_date: datetime.date = None,
		booster: t.Tuple[str] = None,
		border: Border = None,
		magic_card_info_code: str = None,
		gatherer_code: str = None,
		mkm_name: str = None,
		mkm_id: int = None,
	):
		self._name = name
		self._code = code
		self._release_date = release_date
		self._booster = booster
		self._border = border
		self._magic_card_info_code = magic_card_info_code
		self._gatherer_code = gatherer_code
		self._mkm_name = mkm_name
		self._mkm_id = mkm_id
		self.printings = Many(self, '_expansion')
	@property
	def name(self):
		return self._name
	@property
	def code(self):
		return self._code
	@property
	def release_date(self):
		return self.release_date
	@property
	def booster(self):
		return self._booster
	@property
	def border(self):
		return self._border
	@property
	def magic_card_info_code(self):
		return self._magic_card_info_code
	@property
	def gatherer_code(self):
		return self._gatherer_code
	@property
	def mkm_name(self):
		return self._mkm_name
	@property
	def mkm_id(self):
		return self._mkm_id
