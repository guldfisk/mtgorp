# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/search/search_grammar.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2$")
        buf.write("\u0191\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\3\2\3\2\3\3")
        buf.write("\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16l\n\16\3\17\3")
        buf.write("\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\5\17w\n\17\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\20\5\20\u008a\n\20\3\21\3\21\3")
        buf.write("\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21\u0096\n\21")
        buf.write("\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\5\22\u00a5\n\22\3\23\3\23\3\23\3\23\3\23\3")
        buf.write("\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5\23\u00b5")
        buf.write("\n\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\5\24\u00ce\n\24\3\25\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u00de")
        buf.write("\n\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\5\26\u00ec\n\26\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\5\27\u00f4\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\30\5\30\u0102\n\30\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\5\31")
        buf.write("\u0110\n\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3")
        buf.write("\32\3\32\5\32\u011c\n\32\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\5\33\u012a\n\33\3\34\3")
        buf.write("\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u013f\n\34\3")
        buf.write("\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\5\35")
        buf.write("\u014b\n\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3")
        buf.write("\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\5\36\u0163\n\36\3\37\3\37\3\37\3\37\3")
        buf.write("\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3\37\3\37\3\37\3\37\5\37\u0179\n\37\3 \6 \u017c")
        buf.write("\n \r \16 \u017d\3!\3!\7!\u0182\n!\f!\16!\u0185\13!\3")
        buf.write("!\3!\3\"\6\"\u018a\n\"\r\"\16\"\u018b\3#\3#\3#\3#\2\2")
        buf.write("$\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31")
        buf.write("\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$\3\2\f\4\2")
        buf.write("PPpp\4\2VVvv\4\2OOoo\4\2QQqq\4\2IIii\4\2GGgg\3\2\62;\3")
        buf.write("\2$$\16\2##)),/\61<C\\c}\177\177\u00e2\u00e4\u00eb\u00eb")
        buf.write("\u00ef\u00ef\u00f8\u00f8\u00fc\u00fd\5\2\13\f\17\17\"")
        buf.write("\"\2\u01b3\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2")
        buf.write("\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2")
        buf.write("\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2")
        buf.write("\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#")
        buf.write("\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65")
        buf.write("\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2")
        buf.write("\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\3G\3\2\2")
        buf.write("\2\5I\3\2\2\2\7K\3\2\2\2\tM\3\2\2\2\13O\3\2\2\2\rR\3\2")
        buf.write("\2\2\17T\3\2\2\2\21V\3\2\2\2\23X\3\2\2\2\25[\3\2\2\2\27")
        buf.write("]\3\2\2\2\31`\3\2\2\2\33k\3\2\2\2\35v\3\2\2\2\37\u0089")
        buf.write("\3\2\2\2!\u0095\3\2\2\2#\u00a4\3\2\2\2%\u00b4\3\2\2\2")
        buf.write("\'\u00cd\3\2\2\2)\u00dd\3\2\2\2+\u00eb\3\2\2\2-\u00f3")
        buf.write("\3\2\2\2/\u0101\3\2\2\2\61\u010f\3\2\2\2\63\u011b\3\2")
        buf.write("\2\2\65\u0129\3\2\2\2\67\u013e\3\2\2\29\u014a\3\2\2\2")
        buf.write(";\u0162\3\2\2\2=\u0178\3\2\2\2?\u017b\3\2\2\2A\u017f\3")
        buf.write("\2\2\2C\u0189\3\2\2\2E\u018d\3\2\2\2GH\7#\2\2H\4\3\2\2")
        buf.write("\2IJ\7*\2\2J\6\3\2\2\2KL\7+\2\2L\b\3\2\2\2MN\7(\2\2N\n")
        buf.write("\3\2\2\2OP\7~\2\2PQ\7~\2\2Q\f\3\2\2\2RS\7?\2\2S\16\3\2")
        buf.write("\2\2TU\7=\2\2U\20\3\2\2\2VW\7>\2\2W\22\3\2\2\2XY\7>\2")
        buf.write("\2YZ\7?\2\2Z\24\3\2\2\2[\\\7@\2\2\\\26\3\2\2\2]^\7@\2")
        buf.write("\2^_\7?\2\2_\30\3\2\2\2`a\7B\2\2a\32\3\2\2\2bl\t\2\2\2")
        buf.write("cd\7p\2\2de\7c\2\2ef\7o\2\2fl\7g\2\2gh\7P\2\2hi\7C\2\2")
        buf.write("ij\7O\2\2jl\7G\2\2kb\3\2\2\2kc\3\2\2\2kg\3\2\2\2l\34\3")
        buf.write("\2\2\2mw\t\3\2\2no\7v\2\2op\7{\2\2pq\7r\2\2qw\7g\2\2r")
        buf.write("s\7v\2\2st\7{\2\2tu\7r\2\2uw\7g\2\2vm\3\2\2\2vn\3\2\2")
        buf.write("\2vr\3\2\2\2w\36\3\2\2\2x\u008a\t\4\2\2yz\7o\2\2z{\7c")
        buf.write("\2\2{|\7p\2\2|}\7c\2\2}~\7e\2\2~\177\7q\2\2\177\u0080")
        buf.write("\7u\2\2\u0080\u008a\7v\2\2\u0081\u0082\7O\2\2\u0082\u0083")
        buf.write("\7C\2\2\u0083\u0084\7P\2\2\u0084\u0085\7C\2\2\u0085\u0086")
        buf.write("\7E\2\2\u0086\u0087\7Q\2\2\u0087\u0088\7U\2\2\u0088\u008a")
        buf.write("\7V\2\2\u0089x\3\2\2\2\u0089y\3\2\2\2\u0089\u0081\3\2")
        buf.write("\2\2\u008a \3\2\2\2\u008b\u008c\7e\2\2\u008c\u008d\7q")
        buf.write("\2\2\u008d\u008e\7n\2\2\u008e\u008f\7q\2\2\u008f\u0096")
        buf.write("\7t\2\2\u0090\u0091\7E\2\2\u0091\u0092\7Q\2\2\u0092\u0093")
        buf.write("\7N\2\2\u0093\u0094\7Q\2\2\u0094\u0096\7T\2\2\u0095\u008b")
        buf.write("\3\2\2\2\u0095\u0090\3\2\2\2\u0096\"\3\2\2\2\u0097\u00a5")
        buf.write("\t\5\2\2\u0098\u0099\7q\2\2\u0099\u009a\7t\2\2\u009a\u009b")
        buf.write("\7c\2\2\u009b\u009c\7e\2\2\u009c\u009d\7n\2\2\u009d\u00a5")
        buf.write("\7g\2\2\u009e\u009f\7Q\2\2\u009f\u00a0\7T\2\2\u00a0\u00a1")
        buf.write("\7C\2\2\u00a1\u00a2\7E\2\2\u00a2\u00a3\7N\2\2\u00a3\u00a5")
        buf.write("\7G\2\2\u00a4\u0097\3\2\2\2\u00a4\u0098\3\2\2\2\u00a4")
        buf.write("\u009e\3\2\2\2\u00a5$\3\2\2\2\u00a6\u00a7\7r\2\2\u00a7")
        buf.write("\u00a8\7q\2\2\u00a8\u00a9\7y\2\2\u00a9\u00aa\7g\2\2\u00aa")
        buf.write("\u00b5\7t\2\2\u00ab\u00ac\7R\2\2\u00ac\u00ad\7Q\2\2\u00ad")
        buf.write("\u00ae\7Y\2\2\u00ae\u00af\7G\2\2\u00af\u00b5\7T\2\2\u00b0")
        buf.write("\u00b1\7r\2\2\u00b1\u00b5\7q\2\2\u00b2\u00b3\7R\2\2\u00b3")
        buf.write("\u00b5\7Q\2\2\u00b4\u00a6\3\2\2\2\u00b4\u00ab\3\2\2\2")
        buf.write("\u00b4\u00b0\3\2\2\2\u00b4\u00b2\3\2\2\2\u00b5&\3\2\2")
        buf.write("\2\u00b6\u00ce\t\6\2\2\u00b7\u00b8\7v\2\2\u00b8\u00b9")
        buf.write("\7q\2\2\u00b9\u00ba\7w\2\2\u00ba\u00bb\7i\2\2\u00bb\u00bc")
        buf.write("\7j\2\2\u00bc\u00bd\7p\2\2\u00bd\u00be\7g\2\2\u00be\u00bf")
        buf.write("\7u\2\2\u00bf\u00ce\7u\2\2\u00c0\u00c1\7V\2\2\u00c1\u00c2")
        buf.write("\7Q\2\2\u00c2\u00c3\7W\2\2\u00c3\u00c4\7I\2\2\u00c4\u00c5")
        buf.write("\7J\2\2\u00c5\u00c6\7P\2\2\u00c6\u00c7\7G\2\2\u00c7\u00c8")
        buf.write("\7U\2\2\u00c8\u00ce\7U\2\2\u00c9\u00ca\7v\2\2\u00ca\u00ce")
        buf.write("\7q\2\2\u00cb\u00cc\7V\2\2\u00cc\u00ce\7Q\2\2\u00cd\u00b6")
        buf.write("\3\2\2\2\u00cd\u00b7\3\2\2\2\u00cd\u00c0\3\2\2\2\u00cd")
        buf.write("\u00c9\3\2\2\2\u00cd\u00cb\3\2\2\2\u00ce(\3\2\2\2\u00cf")
        buf.write("\u00d0\7n\2\2\u00d0\u00d1\7q\2\2\u00d1\u00d2\7{\2\2\u00d2")
        buf.write("\u00d3\7c\2\2\u00d3\u00d4\7n\2\2\u00d4\u00d5\7v\2\2\u00d5")
        buf.write("\u00de\7{\2\2\u00d6\u00d7\7N\2\2\u00d7\u00d8\7Q\2\2\u00d8")
        buf.write("\u00d9\7[\2\2\u00d9\u00da\7C\2\2\u00da\u00db\7N\2\2\u00db")
        buf.write("\u00dc\7V\2\2\u00dc\u00de\7[\2\2\u00dd\u00cf\3\2\2\2\u00dd")
        buf.write("\u00d6\3\2\2\2\u00de*\3\2\2\2\u00df\u00e0\7c\2\2\u00e0")
        buf.write("\u00e1\7t\2\2\u00e1\u00e2\7v\2\2\u00e2\u00e3\7k\2\2\u00e3")
        buf.write("\u00e4\7u\2\2\u00e4\u00ec\7v\2\2\u00e5\u00e6\7C\2\2\u00e6")
        buf.write("\u00e7\7T\2\2\u00e7\u00e8\7V\2\2\u00e8\u00e9\7K\2\2\u00e9")
        buf.write("\u00ea\7U\2\2\u00ea\u00ec\7V\2\2\u00eb\u00df\3\2\2\2\u00eb")
        buf.write("\u00e5\3\2\2\2\u00ec,\3\2\2\2\u00ed\u00ee\7e\2\2\u00ee")
        buf.write("\u00ef\7o\2\2\u00ef\u00f4\7e\2\2\u00f0\u00f1\7E\2\2\u00f1")
        buf.write("\u00f2\7O\2\2\u00f2\u00f4\7E\2\2\u00f3\u00ed\3\2\2\2\u00f3")
        buf.write("\u00f0\3\2\2\2\u00f4.\3\2\2\2\u00f5\u00f6\7t\2\2\u00f6")
        buf.write("\u00f7\7c\2\2\u00f7\u00f8\7t\2\2\u00f8\u00f9\7k\2\2\u00f9")
        buf.write("\u00fa\7v\2\2\u00fa\u0102\7{\2\2\u00fb\u00fc\7T\2\2\u00fc")
        buf.write("\u00fd\7C\2\2\u00fd\u00fe\7T\2\2\u00fe\u00ff\7K\2\2\u00ff")
        buf.write("\u0100\7V\2\2\u0100\u0102\7[\2\2\u0101\u00f5\3\2\2\2\u0101")
        buf.write("\u00fb\3\2\2\2\u0102\60\3\2\2\2\u0103\u0104\7n\2\2\u0104")
        buf.write("\u0105\7c\2\2\u0105\u0106\7{\2\2\u0106\u0107\7q\2\2\u0107")
        buf.write("\u0108\7w\2\2\u0108\u0110\7v\2\2\u0109\u010a\7N\2\2\u010a")
        buf.write("\u010b\7C\2\2\u010b\u010c\7[\2\2\u010c\u010d\7Q\2\2\u010d")
        buf.write("\u010e\7W\2\2\u010e\u0110\7V\2\2\u010f\u0103\3\2\2\2\u010f")
        buf.write("\u0109\3\2\2\2\u0110\62\3\2\2\2\u0111\u0112\7h\2\2\u0112")
        buf.write("\u0113\7n\2\2\u0113\u0114\7c\2\2\u0114\u0115\7i\2\2\u0115")
        buf.write("\u011c\7u\2\2\u0116\u0117\7H\2\2\u0117\u0118\7N\2\2\u0118")
        buf.write("\u0119\7C\2\2\u0119\u011a\7I\2\2\u011a\u011c\7U\2\2\u011b")
        buf.write("\u0111\3\2\2\2\u011b\u0116\3\2\2\2\u011c\64\3\2\2\2\u011d")
        buf.write("\u011e\7h\2\2\u011e\u011f\7n\2\2\u011f\u0120\7c\2\2\u0120")
        buf.write("\u0121\7x\2\2\u0121\u0122\7q\2\2\u0122\u012a\7t\2\2\u0123")
        buf.write("\u0124\7H\2\2\u0124\u0125\7N\2\2\u0125\u0126\7C\2\2\u0126")
        buf.write("\u0127\7X\2\2\u0127\u0128\7Q\2\2\u0128\u012a\7T\2\2\u0129")
        buf.write("\u011d\3\2\2\2\u0129\u0123\3\2\2\2\u012a\66\3\2\2\2\u012b")
        buf.write("\u013f\t\7\2\2\u012c\u012d\7g\2\2\u012d\u012e\7z\2\2\u012e")
        buf.write("\u012f\7r\2\2\u012f\u0130\7c\2\2\u0130\u0131\7p\2\2\u0131")
        buf.write("\u0132\7u\2\2\u0132\u0133\7k\2\2\u0133\u0134\7q\2\2\u0134")
        buf.write("\u013f\7p\2\2\u0135\u0136\7G\2\2\u0136\u0137\7Z\2\2\u0137")
        buf.write("\u0138\7R\2\2\u0138\u0139\7C\2\2\u0139\u013a\7P\2\2\u013a")
        buf.write("\u013b\7U\2\2\u013b\u013c\7K\2\2\u013c\u013d\7Q\2\2\u013d")
        buf.write("\u013f\7P\2\2\u013e\u012b\3\2\2\2\u013e\u012c\3\2\2\2")
        buf.write("\u013e\u0135\3\2\2\2\u013f8\3\2\2\2\u0140\u0141\7d\2\2")
        buf.write("\u0141\u0142\7n\2\2\u0142\u0143\7q\2\2\u0143\u0144\7e")
        buf.write("\2\2\u0144\u014b\7m\2\2\u0145\u0146\7D\2\2\u0146\u0147")
        buf.write("\7N\2\2\u0147\u0148\7Q\2\2\u0148\u0149\7E\2\2\u0149\u014b")
        buf.write("\7M\2\2\u014a\u0140\3\2\2\2\u014a\u0145\3\2\2\2\u014b")
        buf.write(":\3\2\2\2\u014c\u014d\7e\2\2\u014d\u0163\7c\2\2\u014e")
        buf.write("\u014f\7E\2\2\u014f\u0163\7C\2\2\u0150\u0151\7e\2\2\u0151")
        buf.write("\u0152\7c\2\2\u0152\u0153\7t\2\2\u0153\u0154\7f\2\2\u0154")
        buf.write("\u0155\7d\2\2\u0155\u0156\7q\2\2\u0156\u0157\7c\2\2\u0157")
        buf.write("\u0158\7t\2\2\u0158\u0163\7f\2\2\u0159\u015a\7E\2\2\u015a")
        buf.write("\u015b\7C\2\2\u015b\u015c\7T\2\2\u015c\u015d\7F\2\2\u015d")
        buf.write("\u015e\7D\2\2\u015e\u015f\7Q\2\2\u015f\u0160\7C\2\2\u0160")
        buf.write("\u0161\7T\2\2\u0161\u0163\7F\2\2\u0162\u014c\3\2\2\2\u0162")
        buf.write("\u014e\3\2\2\2\u0162\u0150\3\2\2\2\u0162\u0159\3\2\2\2")
        buf.write("\u0163<\3\2\2\2\u0164\u0165\7r\2\2\u0165\u0179\7t\2\2")
        buf.write("\u0166\u0167\7R\2\2\u0167\u0179\7T\2\2\u0168\u0169\7r")
        buf.write("\2\2\u0169\u016a\7t\2\2\u016a\u016b\7k\2\2\u016b\u016c")
        buf.write("\7p\2\2\u016c\u016d\7v\2\2\u016d\u016e\7k\2\2\u016e\u016f")
        buf.write("\7p\2\2\u016f\u0179\7i\2\2\u0170\u0171\7R\2\2\u0171\u0172")
        buf.write("\7T\2\2\u0172\u0173\7K\2\2\u0173\u0174\7P\2\2\u0174\u0175")
        buf.write("\7V\2\2\u0175\u0176\7K\2\2\u0176\u0177\7P\2\2\u0177\u0179")
        buf.write("\7I\2\2\u0178\u0164\3\2\2\2\u0178\u0166\3\2\2\2\u0178")
        buf.write("\u0168\3\2\2\2\u0178\u0170\3\2\2\2\u0179>\3\2\2\2\u017a")
        buf.write("\u017c\t\b\2\2\u017b\u017a\3\2\2\2\u017c\u017d\3\2\2\2")
        buf.write("\u017d\u017b\3\2\2\2\u017d\u017e\3\2\2\2\u017e@\3\2\2")
        buf.write("\2\u017f\u0183\7$\2\2\u0180\u0182\n\t\2\2\u0181\u0180")
        buf.write("\3\2\2\2\u0182\u0185\3\2\2\2\u0183\u0181\3\2\2\2\u0183")
        buf.write("\u0184\3\2\2\2\u0184\u0186\3\2\2\2\u0185\u0183\3\2\2\2")
        buf.write("\u0186\u0187\7$\2\2\u0187B\3\2\2\2\u0188\u018a\t\n\2\2")
        buf.write("\u0189\u0188\3\2\2\2\u018a\u018b\3\2\2\2\u018b\u0189\3")
        buf.write("\2\2\2\u018b\u018c\3\2\2\2\u018cD\3\2\2\2\u018d\u018e")
        buf.write("\t\13\2\2\u018e\u018f\3\2\2\2\u018f\u0190\b#\2\2\u0190")
        buf.write("F\3\2\2\2\30\2kv\u0089\u0095\u00a4\u00b4\u00cd\u00dd\u00eb")
        buf.write("\u00f3\u0101\u010f\u011b\u0129\u013e\u014a\u0162\u0178")
        buf.write("\u017d\u0183\u018b\3\b\2\2")
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
    COLOR_CODE = 16
    ORACLE_CODE = 17
    POWER_CODE = 18
    TOUGHNESS_CODE = 19
    LOYALTY_CODE = 20
    ARTIST_CODE = 21
    CMC_CODE = 22
    RARITY_CODE = 23
    LAYOUT_CODE = 24
    FLAGS_CODE = 25
    FLAVOR_CODE = 26
    EXPANSION_CODE = 27
    BLOCK_CODE = 28
    CARDBOARD_CODE = 29
    PRINTING_CODE = 30
    UNSIGNED_INTEGER = 31
    QUOTED_VALUE = 32
    VALUE = 33
    WHITESPACE = 34

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'!'", "'('", "')'", "'&'", "'||'", "'='", "';'", "'<'", "'<='", 
            "'>'", "'>='", "'@'" ]

    symbolicNames = [ "<INVALID>",
            "DYNAMIC_VALUE", "NAME_CODE", "TYPE_CODE", "MANA_CODE", "COLOR_CODE", 
            "ORACLE_CODE", "POWER_CODE", "TOUGHNESS_CODE", "LOYALTY_CODE", 
            "ARTIST_CODE", "CMC_CODE", "RARITY_CODE", "LAYOUT_CODE", "FLAGS_CODE", 
            "FLAVOR_CODE", "EXPANSION_CODE", "BLOCK_CODE", "CARDBOARD_CODE", 
            "PRINTING_CODE", "UNSIGNED_INTEGER", "QUOTED_VALUE", "VALUE", 
            "WHITESPACE" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "DYNAMIC_VALUE", "NAME_CODE", 
                  "TYPE_CODE", "MANA_CODE", "COLOR_CODE", "ORACLE_CODE", 
                  "POWER_CODE", "TOUGHNESS_CODE", "LOYALTY_CODE", "ARTIST_CODE", 
                  "CMC_CODE", "RARITY_CODE", "LAYOUT_CODE", "FLAGS_CODE", 
                  "FLAVOR_CODE", "EXPANSION_CODE", "BLOCK_CODE", "CARDBOARD_CODE", 
                  "PRINTING_CODE", "UNSIGNED_INTEGER", "QUOTED_VALUE", "VALUE", 
                  "WHITESPACE" ]

    grammarFileName = "search_grammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


