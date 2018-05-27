import typing as t

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from mtgorp.db.database import CardDatabase
from mtgorp.tools.search.pattern import Any, All, Pattern
from mtgorp.tools.parsing.search.gen.search_grammarParser import search_grammarParser
from mtgorp.tools.parsing.search.gen.search_grammarLexer import search_grammarLexer
from mtgorp.tools.parsing.search.visitor import SearchVisitor, AllBuilder, AnyBuilder, PatternTarget
from mtgorp.tools.parsing.exceptions import ParseException


class SearchPatternParseException(ParseException):
	pass


class SearchPatternParseListener(ErrorListener):

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		raise SearchPatternParseException('Syntax error')

	def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
		raise SearchPatternParseException('Conetext sensitivity')


class SearchParser(object):

	def __init__(self, db: CardDatabase):
		self._visitor = SearchVisitor(db)


	@classmethod
	def _build(cls, parsed: t.Union[AllBuilder, AnyBuilder]) -> Pattern:
		return (
			All
			if isinstance(parsed, AllBuilder) else
			Any
		)(
			(
				cls._build(item)
				if isinstance(item, AllBuilder) or isinstance(item, AnyBuilder)
				else item
			) for item in
			parsed
		)

	def parse(self, s: str) -> t.Tuple[Pattern, PatternTarget]:
		parser = search_grammarParser(
			CommonTokenStream(
				search_grammarLexer(
					InputStream(s)
				)
			)
		)

		parser._listeners = [SearchPatternParseListener()]

		pattern_builder, target = self._visitor.visit(parser.start())

		return self._build(pattern_builder), target