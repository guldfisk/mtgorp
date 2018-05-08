import mtgorp.db.attributeparse.parser as parser

from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.db.attributeparse.exceptions import AttributeParseException


class LayoutParseException(AttributeParseException):
	pass


class Parser(parser.Parser):
	LAYOUT_MAP = {
		'normal': Layout.STANDARD,
		'leveler': Layout.STANDARD,
		'double-faced': Layout.TRANSFORM,
		'flip': Layout.FLIP,
		'meld': Layout.MELD,
		'split': Layout.SPLIT,
		'aftermath': Layout.AFTERMATH,
		'sage': Layout.SAGA,
	}

	@staticmethod
	def parse(s: str) -> Layout:
		try:
			return Parser.LAYOUT_MAP[
				s
			]
		except:
			raise LayoutParseException()