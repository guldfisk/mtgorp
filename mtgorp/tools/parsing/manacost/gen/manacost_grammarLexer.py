# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/manacost/manacost_grammar.g4 by ANTLR 4.7
import sys
from io import StringIO
from typing.io import TextIO

from antlr4 import *


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\17")
        buf.write(":\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7")
        buf.write("\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\6\r\65")
        buf.write("\n\r\r\r\16\r\66\3\16\3\16\2\2\17\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\3\2\f\4\2Y")
        buf.write("Yyy\4\2WWww\4\2DDdd\4\2TTtt\4\2IIii\4\2RRrr\4\2UUuu\4")
        buf.write("\2EEee\3\2\62;\4\2ZZzz\2:\2\3\3\2\2\2\2\5\3\2\2\2\2\7")
        buf.write("\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2")
        buf.write("\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2")
        buf.write("\2\2\31\3\2\2\2\2\33\3\2\2\2\3\35\3\2\2\2\5\37\3\2\2\2")
        buf.write("\7!\3\2\2\2\t#\3\2\2\2\13%\3\2\2\2\r'\3\2\2\2\17)\3\2")
        buf.write("\2\2\21+\3\2\2\2\23-\3\2\2\2\25/\3\2\2\2\27\61\3\2\2\2")
        buf.write("\31\64\3\2\2\2\338\3\2\2\2\35\36\7}\2\2\36\4\3\2\2\2\37")
        buf.write(' \7\177\2\2 \6\3\2\2\2!"\7\61\2\2"\b\3\2\2\2#$\t\2\2')
        buf.write("\2$\n\3\2\2\2%&\t\3\2\2&\f\3\2\2\2'(\t\4\2\2(\16\3\2")
        buf.write("\2\2)*\t\5\2\2*\20\3\2\2\2+,\t\6\2\2,\22\3\2\2\2-.\t\7")
        buf.write("\2\2.\24\3\2\2\2/\60\t\b\2\2\60\26\3\2\2\2\61\62\t\t\2")
        buf.write("\2\62\30\3\2\2\2\63\65\t\n\2\2\64\63\3\2\2\2\65\66\3\2")
        buf.write("\2\2\66\64\3\2\2\2\66\67\3\2\2\2\67\32\3\2\2\289\t\13")
        buf.write("\2\29\34\3\2\2\2\4\2\66\2")
        return buf.getvalue()


class manacost_grammarLexer(Lexer):
    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    WHITE_SYMBOL = 4
    BLUE_SYMBOL = 5
    BLACK_SYMBOL = 6
    RED_SYMBOL = 7
    GREEN_SYMBOL = 8
    PHYREXIAN_SYMBOL = 9
    SNOW_SYMBOL = 10
    COLORLESS_SYMBOL = 11
    GENERIC_SYMBOL = 12
    VARIABLE_SYMBOL = 13

    channelNames = ["DEFAULT_TOKEN_CHANNEL", "HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>", "'{'", "'}'", "'/'"]

    symbolicNames = [
        "<INVALID>",
        "WHITE_SYMBOL",
        "BLUE_SYMBOL",
        "BLACK_SYMBOL",
        "RED_SYMBOL",
        "GREEN_SYMBOL",
        "PHYREXIAN_SYMBOL",
        "SNOW_SYMBOL",
        "COLORLESS_SYMBOL",
        "GENERIC_SYMBOL",
        "VARIABLE_SYMBOL",
    ]

    ruleNames = [
        "T__0",
        "T__1",
        "T__2",
        "WHITE_SYMBOL",
        "BLUE_SYMBOL",
        "BLACK_SYMBOL",
        "RED_SYMBOL",
        "GREEN_SYMBOL",
        "PHYREXIAN_SYMBOL",
        "SNOW_SYMBOL",
        "COLORLESS_SYMBOL",
        "GENERIC_SYMBOL",
        "VARIABLE_SYMBOL",
    ]

    grammarFileName = "manacost_grammar.g4"

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
