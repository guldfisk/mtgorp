import re

import mtgorp.db.attributeparse.parser as parser

from mtgorp.db.attributeparse.exceptions import AttributeParseException
from mtgorp.models.persistent.attributes.powertoughness import PTValue


class LoyaltyParseException(AttributeParseException):
	pass


class Parser(parser.Parser):
	matcher = re.compile('\\d+')

	@staticmethod
	def parse(s: str) -> PTValue:
		if not Parser.matcher.match(s):
			return PTValue(variable=True)

		return PTValue(int(s))