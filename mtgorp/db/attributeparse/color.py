import mtgorp.db.attributeparse.parser as parser

from mtgorp.models.persistent.attributes.colors import Color
from mtgorp.db.attributeparse.exceptions import AttributeParseException


class ColorParseException(AttributeParseException):
	pass


class Parser(parser.Parser):
	switch = {
		'W': Color.WHITE,
		'WHITE': Color.WHITE,
		'U': Color.BLUE,
		'BLUE': Color.BLUE,
		'B': Color.BLACK,
		'BLACK': Color.BLACK,
		'R': Color.RED,
		'RED': Color.RED,
		'G': Color.GREEN,
		'GREEN': Color.GREEN
	}
	
	@staticmethod
	def parse(s: str) -> Color:
		try:
			return Parser.switch[s.upper()]
		except KeyError:
			raise ColorParseException()
