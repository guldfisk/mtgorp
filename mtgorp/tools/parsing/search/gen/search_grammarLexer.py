# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/search/search_grammar.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2#")
        buf.write("\u0183\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\3\2\3\2\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n")
        buf.write("\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\5\16j\n\16\3\17\3\17\3")
        buf.write("\17\3\17\3\17\3\17\3\17\3\17\3\17\5\17u\n\17\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\5\20\u0088\n\20\3\21\3\21\3\21\3")
        buf.write("\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21")
        buf.write("\u0097\n\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\5\22\u00a7\n\22\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5\23")
        buf.write("\u00c0\n\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\5\24\u00d0\n\24\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25")
        buf.write("\u00de\n\25\3\26\3\26\3\26\3\26\3\26\3\26\5\26\u00e6\n")
        buf.write("\26\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\5\27\u00f4\n\27\3\30\3\30\3\30\3\30\3\30\3")
        buf.write("\30\3\30\3\30\3\30\3\30\3\30\3\30\5\30\u0102\n\30\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\5\31\u010e")
        buf.write("\n\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\5\32\u011c\n\32\3\33\3\33\3\33\3\33\3\33\3")
        buf.write("\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\5\33\u0131\n\33\3\34\3\34\3\34\3\34\3")
        buf.write("\34\3\34\3\34\3\34\3\34\3\34\5\34\u013d\n\34\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\5\35\u0155")
        buf.write("\n\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\5\36")
        buf.write("\u016b\n\36\3\37\6\37\u016e\n\37\r\37\16\37\u016f\3 \3")
        buf.write(" \7 \u0174\n \f \16 \u0177\13 \3 \3 \3!\6!\u017c\n!\r")
        buf.write("!\16!\u017d\3\"\3\"\3\"\3\"\2\2#\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21")
        buf.write("!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#\3\2\f\4\2PPpp\4\2VVvv\4\2OOoo\4\2")
        buf.write("QQqq\4\2IIii\4\2GGgg\3\2\62;\3\2$$\16\2##)),/\61<C\\c")
        buf.write("}\177\177\u00e2\u00e4\u00eb\u00eb\u00ef\u00ef\u00f8\u00f8")
        buf.write("\u00fc\u00fd\5\2\13\f\17\17\"\"\2\u01a4\2\3\3\2\2\2\2")
        buf.write("\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3")
        buf.write("\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2")
        buf.write("\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2")
        buf.write("\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3")
        buf.write("\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61")
        buf.write("\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2")
        buf.write("\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3")
        buf.write("\2\2\2\3E\3\2\2\2\5G\3\2\2\2\7I\3\2\2\2\tK\3\2\2\2\13")
        buf.write("M\3\2\2\2\rP\3\2\2\2\17R\3\2\2\2\21T\3\2\2\2\23V\3\2\2")
        buf.write("\2\25Y\3\2\2\2\27[\3\2\2\2\31^\3\2\2\2\33i\3\2\2\2\35")
        buf.write("t\3\2\2\2\37\u0087\3\2\2\2!\u0096\3\2\2\2#\u00a6\3\2\2")
        buf.write("\2%\u00bf\3\2\2\2\'\u00cf\3\2\2\2)\u00dd\3\2\2\2+\u00e5")
        buf.write("\3\2\2\2-\u00f3\3\2\2\2/\u0101\3\2\2\2\61\u010d\3\2\2")
        buf.write("\2\63\u011b\3\2\2\2\65\u0130\3\2\2\2\67\u013c\3\2\2\2")
        buf.write("9\u0154\3\2\2\2;\u016a\3\2\2\2=\u016d\3\2\2\2?\u0171\3")
        buf.write("\2\2\2A\u017b\3\2\2\2C\u017f\3\2\2\2EF\7#\2\2F\4\3\2\2")
        buf.write("\2GH\7*\2\2H\6\3\2\2\2IJ\7+\2\2J\b\3\2\2\2KL\7(\2\2L\n")
        buf.write("\3\2\2\2MN\7~\2\2NO\7~\2\2O\f\3\2\2\2PQ\7?\2\2Q\16\3\2")
        buf.write("\2\2RS\7=\2\2S\20\3\2\2\2TU\7>\2\2U\22\3\2\2\2VW\7>\2")
        buf.write("\2WX\7?\2\2X\24\3\2\2\2YZ\7@\2\2Z\26\3\2\2\2[\\\7@\2\2")
        buf.write("\\]\7?\2\2]\30\3\2\2\2^_\7B\2\2_\32\3\2\2\2`j\t\2\2\2")
        buf.write("ab\7p\2\2bc\7c\2\2cd\7o\2\2dj\7g\2\2ef\7P\2\2fg\7C\2\2")
        buf.write("gh\7O\2\2hj\7G\2\2i`\3\2\2\2ia\3\2\2\2ie\3\2\2\2j\34\3")
        buf.write("\2\2\2ku\t\3\2\2lm\7v\2\2mn\7{\2\2no\7r\2\2ou\7g\2\2p")
        buf.write("q\7v\2\2qr\7{\2\2rs\7r\2\2su\7g\2\2tk\3\2\2\2tl\3\2\2")
        buf.write("\2tp\3\2\2\2u\36\3\2\2\2v\u0088\t\4\2\2wx\7o\2\2xy\7c")
        buf.write("\2\2yz\7p\2\2z{\7c\2\2{|\7e\2\2|}\7q\2\2}~\7u\2\2~\u0088")
        buf.write("\7v\2\2\177\u0080\7O\2\2\u0080\u0081\7C\2\2\u0081\u0082")
        buf.write("\7P\2\2\u0082\u0083\7C\2\2\u0083\u0084\7E\2\2\u0084\u0085")
        buf.write("\7Q\2\2\u0085\u0086\7U\2\2\u0086\u0088\7V\2\2\u0087v\3")
        buf.write("\2\2\2\u0087w\3\2\2\2\u0087\177\3\2\2\2\u0088 \3\2\2\2")
        buf.write("\u0089\u0097\t\5\2\2\u008a\u008b\7q\2\2\u008b\u008c\7")
        buf.write("t\2\2\u008c\u008d\7c\2\2\u008d\u008e\7e\2\2\u008e\u008f")
        buf.write("\7n\2\2\u008f\u0097\7g\2\2\u0090\u0091\7Q\2\2\u0091\u0092")
        buf.write("\7T\2\2\u0092\u0093\7C\2\2\u0093\u0094\7E\2\2\u0094\u0095")
        buf.write("\7N\2\2\u0095\u0097\7G\2\2\u0096\u0089\3\2\2\2\u0096\u008a")
        buf.write("\3\2\2\2\u0096\u0090\3\2\2\2\u0097\"\3\2\2\2\u0098\u0099")
        buf.write("\7r\2\2\u0099\u009a\7q\2\2\u009a\u009b\7y\2\2\u009b\u009c")
        buf.write("\7g\2\2\u009c\u00a7\7t\2\2\u009d\u009e\7R\2\2\u009e\u009f")
        buf.write("\7Q\2\2\u009f\u00a0\7Y\2\2\u00a0\u00a1\7G\2\2\u00a1\u00a7")
        buf.write("\7T\2\2\u00a2\u00a3\7r\2\2\u00a3\u00a7\7q\2\2\u00a4\u00a5")
        buf.write("\7R\2\2\u00a5\u00a7\7Q\2\2\u00a6\u0098\3\2\2\2\u00a6\u009d")
        buf.write("\3\2\2\2\u00a6\u00a2\3\2\2\2\u00a6\u00a4\3\2\2\2\u00a7")
        buf.write("$\3\2\2\2\u00a8\u00c0\t\6\2\2\u00a9\u00aa\7v\2\2\u00aa")
        buf.write("\u00ab\7q\2\2\u00ab\u00ac\7w\2\2\u00ac\u00ad\7i\2\2\u00ad")
        buf.write("\u00ae\7j\2\2\u00ae\u00af\7p\2\2\u00af\u00b0\7g\2\2\u00b0")
        buf.write("\u00b1\7u\2\2\u00b1\u00c0\7u\2\2\u00b2\u00b3\7V\2\2\u00b3")
        buf.write("\u00b4\7Q\2\2\u00b4\u00b5\7W\2\2\u00b5\u00b6\7I\2\2\u00b6")
        buf.write("\u00b7\7J\2\2\u00b7\u00b8\7P\2\2\u00b8\u00b9\7G\2\2\u00b9")
        buf.write("\u00ba\7U\2\2\u00ba\u00c0\7U\2\2\u00bb\u00bc\7v\2\2\u00bc")
        buf.write("\u00c0\7q\2\2\u00bd\u00be\7V\2\2\u00be\u00c0\7Q\2\2\u00bf")
        buf.write("\u00a8\3\2\2\2\u00bf\u00a9\3\2\2\2\u00bf\u00b2\3\2\2\2")
        buf.write("\u00bf\u00bb\3\2\2\2\u00bf\u00bd\3\2\2\2\u00c0&\3\2\2")
        buf.write("\2\u00c1\u00c2\7n\2\2\u00c2\u00c3\7q\2\2\u00c3\u00c4\7")
        buf.write("{\2\2\u00c4\u00c5\7c\2\2\u00c5\u00c6\7n\2\2\u00c6\u00c7")
        buf.write("\7v\2\2\u00c7\u00d0\7{\2\2\u00c8\u00c9\7N\2\2\u00c9\u00ca")
        buf.write("\7Q\2\2\u00ca\u00cb\7[\2\2\u00cb\u00cc\7C\2\2\u00cc\u00cd")
        buf.write("\7N\2\2\u00cd\u00ce\7V\2\2\u00ce\u00d0\7[\2\2\u00cf\u00c1")
        buf.write("\3\2\2\2\u00cf\u00c8\3\2\2\2\u00d0(\3\2\2\2\u00d1\u00d2")
        buf.write("\7c\2\2\u00d2\u00d3\7t\2\2\u00d3\u00d4\7v\2\2\u00d4\u00d5")
        buf.write("\7k\2\2\u00d5\u00d6\7u\2\2\u00d6\u00de\7v\2\2\u00d7\u00d8")
        buf.write("\7C\2\2\u00d8\u00d9\7T\2\2\u00d9\u00da\7V\2\2\u00da\u00db")
        buf.write("\7K\2\2\u00db\u00dc\7U\2\2\u00dc\u00de\7V\2\2\u00dd\u00d1")
        buf.write("\3\2\2\2\u00dd\u00d7\3\2\2\2\u00de*\3\2\2\2\u00df\u00e0")
        buf.write("\7e\2\2\u00e0\u00e1\7o\2\2\u00e1\u00e6\7e\2\2\u00e2\u00e3")
        buf.write("\7E\2\2\u00e3\u00e4\7O\2\2\u00e4\u00e6\7E\2\2\u00e5\u00df")
        buf.write("\3\2\2\2\u00e5\u00e2\3\2\2\2\u00e6,\3\2\2\2\u00e7\u00e8")
        buf.write("\7t\2\2\u00e8\u00e9\7c\2\2\u00e9\u00ea\7t\2\2\u00ea\u00eb")
        buf.write("\7k\2\2\u00eb\u00ec\7v\2\2\u00ec\u00f4\7{\2\2\u00ed\u00ee")
        buf.write("\7T\2\2\u00ee\u00ef\7C\2\2\u00ef\u00f0\7T\2\2\u00f0\u00f1")
        buf.write("\7K\2\2\u00f1\u00f2\7V\2\2\u00f2\u00f4\7[\2\2\u00f3\u00e7")
        buf.write("\3\2\2\2\u00f3\u00ed\3\2\2\2\u00f4.\3\2\2\2\u00f5\u00f6")
        buf.write("\7n\2\2\u00f6\u00f7\7c\2\2\u00f7\u00f8\7{\2\2\u00f8\u00f9")
        buf.write("\7q\2\2\u00f9\u00fa\7w\2\2\u00fa\u0102\7v\2\2\u00fb\u00fc")
        buf.write("\7N\2\2\u00fc\u00fd\7C\2\2\u00fd\u00fe\7[\2\2\u00fe\u00ff")
        buf.write("\7Q\2\2\u00ff\u0100\7W\2\2\u0100\u0102\7V\2\2\u0101\u00f5")
        buf.write("\3\2\2\2\u0101\u00fb\3\2\2\2\u0102\60\3\2\2\2\u0103\u0104")
        buf.write("\7h\2\2\u0104\u0105\7n\2\2\u0105\u0106\7c\2\2\u0106\u0107")
        buf.write("\7i\2\2\u0107\u010e\7u\2\2\u0108\u0109\7H\2\2\u0109\u010a")
        buf.write("\7N\2\2\u010a\u010b\7C\2\2\u010b\u010c\7I\2\2\u010c\u010e")
        buf.write("\7U\2\2\u010d\u0103\3\2\2\2\u010d\u0108\3\2\2\2\u010e")
        buf.write("\62\3\2\2\2\u010f\u0110\7h\2\2\u0110\u0111\7n\2\2\u0111")
        buf.write("\u0112\7c\2\2\u0112\u0113\7x\2\2\u0113\u0114\7q\2\2\u0114")
        buf.write("\u011c\7t\2\2\u0115\u0116\7H\2\2\u0116\u0117\7N\2\2\u0117")
        buf.write("\u0118\7C\2\2\u0118\u0119\7X\2\2\u0119\u011a\7Q\2\2\u011a")
        buf.write("\u011c\7T\2\2\u011b\u010f\3\2\2\2\u011b\u0115\3\2\2\2")
        buf.write("\u011c\64\3\2\2\2\u011d\u0131\t\7\2\2\u011e\u011f\7g\2")
        buf.write("\2\u011f\u0120\7z\2\2\u0120\u0121\7r\2\2\u0121\u0122\7")
        buf.write("c\2\2\u0122\u0123\7p\2\2\u0123\u0124\7u\2\2\u0124\u0125")
        buf.write("\7k\2\2\u0125\u0126\7q\2\2\u0126\u0131\7p\2\2\u0127\u0128")
        buf.write("\7G\2\2\u0128\u0129\7Z\2\2\u0129\u012a\7R\2\2\u012a\u012b")
        buf.write("\7C\2\2\u012b\u012c\7P\2\2\u012c\u012d\7U\2\2\u012d\u012e")
        buf.write("\7K\2\2\u012e\u012f\7Q\2\2\u012f\u0131\7P\2\2\u0130\u011d")
        buf.write("\3\2\2\2\u0130\u011e\3\2\2\2\u0130\u0127\3\2\2\2\u0131")
        buf.write("\66\3\2\2\2\u0132\u0133\7d\2\2\u0133\u0134\7n\2\2\u0134")
        buf.write("\u0135\7q\2\2\u0135\u0136\7e\2\2\u0136\u013d\7m\2\2\u0137")
        buf.write("\u0138\7D\2\2\u0138\u0139\7N\2\2\u0139\u013a\7Q\2\2\u013a")
        buf.write("\u013b\7E\2\2\u013b\u013d\7M\2\2\u013c\u0132\3\2\2\2\u013c")
        buf.write("\u0137\3\2\2\2\u013d8\3\2\2\2\u013e\u013f\7e\2\2\u013f")
        buf.write("\u0155\7c\2\2\u0140\u0141\7E\2\2\u0141\u0155\7C\2\2\u0142")
        buf.write("\u0143\7e\2\2\u0143\u0144\7c\2\2\u0144\u0145\7t\2\2\u0145")
        buf.write("\u0146\7f\2\2\u0146\u0147\7d\2\2\u0147\u0148\7q\2\2\u0148")
        buf.write("\u0149\7c\2\2\u0149\u014a\7t\2\2\u014a\u0155\7f\2\2\u014b")
        buf.write("\u014c\7E\2\2\u014c\u014d\7C\2\2\u014d\u014e\7T\2\2\u014e")
        buf.write("\u014f\7F\2\2\u014f\u0150\7D\2\2\u0150\u0151\7Q\2\2\u0151")
        buf.write("\u0152\7C\2\2\u0152\u0153\7T\2\2\u0153\u0155\7F\2\2\u0154")
        buf.write("\u013e\3\2\2\2\u0154\u0140\3\2\2\2\u0154\u0142\3\2\2\2")
        buf.write("\u0154\u014b\3\2\2\2\u0155:\3\2\2\2\u0156\u0157\7r\2\2")
        buf.write("\u0157\u016b\7t\2\2\u0158\u0159\7R\2\2\u0159\u016b\7T")
        buf.write("\2\2\u015a\u015b\7r\2\2\u015b\u015c\7t\2\2\u015c\u015d")
        buf.write("\7k\2\2\u015d\u015e\7p\2\2\u015e\u015f\7v\2\2\u015f\u0160")
        buf.write("\7k\2\2\u0160\u0161\7p\2\2\u0161\u016b\7i\2\2\u0162\u0163")
        buf.write("\7R\2\2\u0163\u0164\7T\2\2\u0164\u0165\7K\2\2\u0165\u0166")
        buf.write("\7P\2\2\u0166\u0167\7V\2\2\u0167\u0168\7K\2\2\u0168\u0169")
        buf.write("\7P\2\2\u0169\u016b\7I\2\2\u016a\u0156\3\2\2\2\u016a\u0158")
        buf.write("\3\2\2\2\u016a\u015a\3\2\2\2\u016a\u0162\3\2\2\2\u016b")
        buf.write("<\3\2\2\2\u016c\u016e\t\b\2\2\u016d\u016c\3\2\2\2\u016e")
        buf.write("\u016f\3\2\2\2\u016f\u016d\3\2\2\2\u016f\u0170\3\2\2\2")
        buf.write("\u0170>\3\2\2\2\u0171\u0175\7$\2\2\u0172\u0174\n\t\2\2")
        buf.write("\u0173\u0172\3\2\2\2\u0174\u0177\3\2\2\2\u0175\u0173\3")
        buf.write("\2\2\2\u0175\u0176\3\2\2\2\u0176\u0178\3\2\2\2\u0177\u0175")
        buf.write("\3\2\2\2\u0178\u0179\7$\2\2\u0179@\3\2\2\2\u017a\u017c")
        buf.write("\t\n\2\2\u017b\u017a\3\2\2\2\u017c\u017d\3\2\2\2\u017d")
        buf.write("\u017b\3\2\2\2\u017d\u017e\3\2\2\2\u017eB\3\2\2\2\u017f")
        buf.write("\u0180\t\13\2\2\u0180\u0181\3\2\2\2\u0181\u0182\b\"\2")
        buf.write("\2\u0182D\3\2\2\2\27\2it\u0087\u0096\u00a6\u00bf\u00cf")
        buf.write("\u00dd\u00e5\u00f3\u0101\u010d\u011b\u0130\u013c\u0154")
        buf.write("\u016a\u016f\u0175\u017d\3\b\2\2")
        return buf.getvalue()


class search_grammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    DYNAMIC_VALUE = 12
    NAME_CODE = 13
    TYPE_CODE = 14
    MANA_CODE = 15
    ORACLE_CODE = 16
    POWER_CODE = 17
    TOUGHNESS_CODE = 18
    LOYALTY_CODE = 19
    ARTIST_CODE = 20
    CMC_CODE = 21
    RARITY_CODE = 22
    LAYOUT_CODE = 23
    FLAGS_CODE = 24
    FLAVOR_CODE = 25
    EXPANSION_CODE = 26
    BLOCK_CODE = 27
    CARDBOARD_CODE = 28
    PRINTING_CODE = 29
    UNSIGNED_INTEGER = 30
    QUOTED_VALUE = 31
    VALUE = 32
    WHITESPACE = 33

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'!'", "'('", "')'", "'&'", "'||'", "'='", "';'", "'<'", "'<='", 
            "'>'", "'>='", "'@'" ]

    symbolicNames = [ "<INVALID>",
            "DYNAMIC_VALUE", "NAME_CODE", "TYPE_CODE", "MANA_CODE", "ORACLE_CODE", 
            "POWER_CODE", "TOUGHNESS_CODE", "LOYALTY_CODE", "ARTIST_CODE", 
            "CMC_CODE", "RARITY_CODE", "LAYOUT_CODE", "FLAGS_CODE", "FLAVOR_CODE", 
            "EXPANSION_CODE", "BLOCK_CODE", "CARDBOARD_CODE", "PRINTING_CODE", 
            "UNSIGNED_INTEGER", "QUOTED_VALUE", "VALUE", "WHITESPACE" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "DYNAMIC_VALUE", "NAME_CODE", 
                  "TYPE_CODE", "MANA_CODE", "ORACLE_CODE", "POWER_CODE", 
                  "TOUGHNESS_CODE", "LOYALTY_CODE", "ARTIST_CODE", "CMC_CODE", 
                  "RARITY_CODE", "LAYOUT_CODE", "FLAGS_CODE", "FLAVOR_CODE", 
                  "EXPANSION_CODE", "BLOCK_CODE", "CARDBOARD_CODE", "PRINTING_CODE", 
                  "UNSIGNED_INTEGER", "QUOTED_VALUE", "VALUE", "WHITESPACE" ]

    grammarFileName = "search_grammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


