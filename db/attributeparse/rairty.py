import db.attributeparse.parser as parser

from models.persistent.attributes.rarities import Rarity
from db.attributeparse.exceptions import AttributeParseException

class RarityParseException(AttributeParseException):
	pass

class Parser(parser.Parser):
	_RARITY_MAP = {
		'Common': Rarity.COMMON,
		'Uncommon': Rarity.UNCOMMON,
		'Rare': Rarity.RARE,
		'Mythic Rare': Rarity.MYTHIC,
		'Basic Land': Rarity.LAND,
		'Special': Rarity.SPECIAL
	}
	@staticmethod
	def parse(s: str) -> Rarity:
		try:
			return Parser._RARITY_MAP[
				s
			]
		except:
			raise RarityParseException()