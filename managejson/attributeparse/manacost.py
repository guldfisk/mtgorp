import re

import typing as t

import managejson.attributeparse.parser as parser

from managejson.attributeparse.exceptions import AttributeParseException
from models.persistent.attributes.manacosts import ManaCostAtom, HybridCostAtom, ManaCost, ONE_GENERIC, SINGULAR_ATOM_MAP

class ManaCostParseException(AttributeParseException):
	pass

class Parser(parser.Parser):
	generic_matcher = re.compile('\\d+$')
	singular_matcher = re.compile('\\w+$')
	matcher = re.compile('[^\\s/]+')
	atom_matcher = re.compile('{([^\\s{}]+)}')
	@staticmethod
	def _parse_cluster_component(s: str) -> t.Iterable[ManaCostAtom]:
		if Parser.generic_matcher.match(s):
			for i in range(int(s)):
				yield ONE_GENERIC
		elif Parser.singular_matcher.match(s):
			try:
				yield SINGULAR_ATOM_MAP[s]
			except KeyError:
				pass
		else:
			raise ManaCostParseException()
	@staticmethod
	def _parse_cluster(s: str) -> t.Iterable[ManaCostAtom]:
		if '/' in s:
			yield HybridCostAtom(
				{
					ManaCost(
						Parser._parse_cluster_component(m.group())
					)
					for m in
					Parser.matcher.finditer(s)
				}
			)
		else:
			for m in Parser.matcher.finditer(s):
				for atom in Parser._parse_cluster_component(m.group()):
					yield atom
	@staticmethod
	def parse(s: str) -> ManaCost:
		return ManaCost(
			atom
			for m in
			Parser.atom_matcher.finditer(s)
			for atom in
			Parser._parse_cluster(m.group(1))
		)
