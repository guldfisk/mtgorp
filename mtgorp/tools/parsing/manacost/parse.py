import typing as t

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from mtgorp.models.persistent.attributes.manacosts import ManaCost, HybridCostAtom

from mtgorp.tools.parsing.exceptions import ParseException

from mtgorp.tools.parsing.manacost.gen.manacost_grammarParser import manacost_grammarParser
from mtgorp.tools.parsing.manacost.gen.manacost_grammarLexer import manacost_grammarLexer

from mtgorp.tools.parsing.manacost.visitor import ManaCostVisitor, ManaCostBuilder, HybridBuilder


class ManaCostParseException(ParseException):
    pass


class ManaCostParseListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ManaCostParseException('Syntax error')

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise ManaCostParseException('Conetext sensitivity')



class ManaCostParser(object):

    def __init__(self):
        self._visitor = ManaCostVisitor()


    @classmethod
    def _build(cls, parsed) -> t.Union[ManaCost, HybridCostAtom]:
        return (
            ManaCost
            if isinstance(parsed, ManaCostBuilder) else
            HybridCostAtom
        )(
            (
                cls._build(item)
                if isinstance(item, ManaCostBuilder) or isinstance(item, HybridBuilder)
                else item
            ) for item in
            parsed
        )

    def parse(self, s: str) -> ManaCost:
        parser = manacost_grammarParser(
            CommonTokenStream(
                manacost_grammarLexer(
                    InputStream(s)
                )
            )
        )

        parser._listeners = [ManaCostParseListener()]

        return self._build(
            self._visitor.visit(
                parser.start()
            )
        )