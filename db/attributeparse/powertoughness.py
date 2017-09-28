import re

import db.attributeparse.parser as parser

from db.attributeparse.exceptions import AttributeParseException
from models.persistent.attributes.powertoughness import PTValue, PowerToughness

class PowerToughnessParseException(AttributeParseException):
	pass

class Parser(parser.Parser):
	matcher = re.compile('([^/]+)/([^/]+)')
	value_matcher = re.compile('-?\\d+')
	@staticmethod
	def parse_ptvalue(s: str) -> PTValue:
		try:
			return PTValue(variable=True) if '*' in s else int(s)
		except ValueError:
			raise PowerToughnessParseException()
	@staticmethod
	def parse(s: str) -> PowerToughness:
		m = Parser.matcher.match(s)
		if not m or len(m.groups()) < 2:
			raise PowerToughnessParseException()
		return PowerToughness(
			Parser.parse_ptvalue(m.group(1)),
			Parser.parse_ptvalue(m.group(2)),
		)
