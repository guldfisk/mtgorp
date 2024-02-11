import typing as t

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from mtgorp.db.database import CardDatabase
from mtgorp.tools.parsing.exceptions import ParseException
from mtgorp.tools.parsing.search.gen.search_grammarLexer import search_grammarLexer
from mtgorp.tools.parsing.search.gen.search_grammarParser import search_grammarParser
from mtgorp.tools.parsing.search.visitor import AllBuilder, AnyBuilder, SearchVisitor
from mtgorp.tools.search.extraction import CardboardStrategy, ExtractionStrategy
from mtgorp.tools.search.pattern import All, Any, Criteria, Pattern


class SearchPatternParseException(ParseException):
    pass


class SearchPatternParseListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SearchPatternParseException("Syntax error")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise SearchPatternParseException("Conetext sensitivity")


class SearchParser(object):
    def __init__(self, db: CardDatabase):
        self._visitor = SearchVisitor(db)

    @classmethod
    def _build(cls, parsed: t.Union[AllBuilder, AnyBuilder]) -> Criteria:
        return (All if isinstance(parsed, AllBuilder) else Any)(
            (cls._build(item) if isinstance(item, AllBuilder) or isinstance(item, AnyBuilder) else item)
            for item in parsed
        )

    def parse_criteria(self, s: str) -> Criteria:
        parser = search_grammarParser(CommonTokenStream(search_grammarLexer(InputStream(s))))

        parser._listeners = [SearchPatternParseListener()]

        return self._build(self._visitor.visit(parser.start()))

    def parse(self, s: str, strategy: t.Type[ExtractionStrategy] = CardboardStrategy) -> Pattern:
        return Pattern(
            self.parse_criteria(s),
            strategy,
        )
