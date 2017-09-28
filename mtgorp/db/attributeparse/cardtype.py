import re

import mtgorp.db.attributeparse.parser as parser

from mtgorp.models.persistent.attributes.cardtypes import CardType, CardTypes, CardSubType, ALL_TYPES
from mtgorp.db.attributeparse.exceptions import AttributeParseException

class CardTypeParseException(AttributeParseException):
	pass

class Parser(parser.Parser):
	card_type_switch = {
		t.name: t for t in ALL_TYPES
	}
	super_type_matcher = re.compile('[^—]*')
	sub_type_matcher = re.compile('.*—(.*)')
	type_matcher = re.compile('\\w+')
	@staticmethod
	def parse(s: str) -> CardTypes:
		super_type_field = Parser.super_type_matcher.match(s)
		if not super_type_field:
			raise CardTypeParseException()
		try:
			super_types = {
				Parser.card_type_switch[m.group()]
				for m in
				Parser.type_matcher.finditer(super_type_field.group())
			}
		except KeyError:
			raise CardTypeParseException()
		sub_type_field = Parser.sub_type_matcher.match(s)
		sub_types = (
			CardSubType(m.group()) for m in Parser.type_matcher.finditer(sub_type_field.group(1))
		) if sub_type_field else ()
		return CardTypes(super_types, sub_types)
