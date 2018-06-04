# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/search/search_grammar.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2$")
        buf.write("\u0187\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\3\2\3\2\3\3")
        buf.write("\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3\r\3\r\3\r\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\5\17n\n")
        buf.write("\17\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\5\20")
        buf.write("y\n\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3")
        buf.write("\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21\u008c\n\21")
        buf.write("\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\5\22\u009b\n\22\3\23\3\23\3\23\3\23\3\23\3")
        buf.write("\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5\23\u00ab")
        buf.write("\n\23\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\5\24\u00c4\n\24\3\25\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u00d4")
        buf.write("\n\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\5\26\u00e2\n\26\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\5\27\u00ea\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\30\5\30\u00f8\n\30\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\5\31")
        buf.write("\u0106\n\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3")
        buf.write("\32\3\32\5\32\u0112\n\32\3\33\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\5\33\u0120\n\33\3\34\3")
        buf.write("\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u0135\n\34\3")
        buf.write("\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\5\35")
        buf.write("\u0141\n\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3")
        buf.write("\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\36\3\36\5\36\u0159\n\36\3\37\3\37\3\37\3\37\3")
        buf.write("\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3\37\3\37\3\37\3\37\5\37\u016f\n\37\3 \6 \u0172")
        buf.write("\n \r \16 \u0173\3!\3!\7!\u0178\n!\f!\16!\u017b\13!\3")
        buf.write("!\3!\3\"\6\"\u0180\n\"\r\"\16\"\u0181\3#\3#\3#\3#\2\2")
        buf.write("$\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31")
        buf.write("\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$\3\2\f\4\2")
        buf.write("PPpp\4\2VVvv\4\2OOoo\4\2QQqq\4\2IIii\4\2GGgg\3\2\62;\3")
        buf.write("\2$$\t\2)),,./\61<C\\c}\177\177\5\2\13\f\17\17\"\"\2\u01a8")
        buf.write("\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13")
        buf.write("\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3")
        buf.write("\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write("\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2")
        buf.write("%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2")
        buf.write("\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67")
        buf.write("\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2")
        buf.write("A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\3G\3\2\2\2\5I\3\2\2\2")
        buf.write("\7K\3\2\2\2\tM\3\2\2\2\13O\3\2\2\2\rQ\3\2\2\2\17T\3\2")
        buf.write("\2\2\21V\3\2\2\2\23X\3\2\2\2\25Z\3\2\2\2\27]\3\2\2\2\31")
        buf.write("_\3\2\2\2\33b\3\2\2\2\35m\3\2\2\2\37x\3\2\2\2!\u008b\3")
        buf.write("\2\2\2#\u009a\3\2\2\2%\u00aa\3\2\2\2\'\u00c3\3\2\2\2)")
        buf.write("\u00d3\3\2\2\2+\u00e1\3\2\2\2-\u00e9\3\2\2\2/\u00f7\3")
        buf.write("\2\2\2\61\u0105\3\2\2\2\63\u0111\3\2\2\2\65\u011f\3\2")
        buf.write("\2\2\67\u0134\3\2\2\29\u0140\3\2\2\2;\u0158\3\2\2\2=\u016e")
        buf.write("\3\2\2\2?\u0171\3\2\2\2A\u0175\3\2\2\2C\u017f\3\2\2\2")
        buf.write("E\u0183\3\2\2\2GH\7%\2\2H\4\3\2\2\2IJ\7#\2\2J\6\3\2\2")
        buf.write("\2KL\7*\2\2L\b\3\2\2\2MN\7+\2\2N\n\3\2\2\2OP\7(\2\2P\f")
        buf.write("\3\2\2\2QR\7~\2\2RS\7~\2\2S\16\3\2\2\2TU\7?\2\2U\20\3")
        buf.write("\2\2\2VW\7=\2\2W\22\3\2\2\2XY\7>\2\2Y\24\3\2\2\2Z[\7>")
        buf.write("\2\2[\\\7?\2\2\\\26\3\2\2\2]^\7@\2\2^\30\3\2\2\2_`\7@")
        buf.write("\2\2`a\7?\2\2a\32\3\2\2\2bc\7B\2\2c\34\3\2\2\2dn\t\2\2")
        buf.write("\2ef\7p\2\2fg\7c\2\2gh\7o\2\2hn\7g\2\2ij\7P\2\2jk\7C\2")
        buf.write("\2kl\7O\2\2ln\7G\2\2md\3\2\2\2me\3\2\2\2mi\3\2\2\2n\36")
        buf.write("\3\2\2\2oy\t\3\2\2pq\7v\2\2qr\7{\2\2rs\7r\2\2sy\7g\2\2")
        buf.write("tu\7v\2\2uv\7{\2\2vw\7r\2\2wy\7g\2\2xo\3\2\2\2xp\3\2\2")
        buf.write("\2xt\3\2\2\2y \3\2\2\2z\u008c\t\4\2\2{|\7o\2\2|}\7c\2")
        buf.write("\2}~\7p\2\2~\177\7c\2\2\177\u0080\7e\2\2\u0080\u0081\7")
        buf.write("q\2\2\u0081\u0082\7u\2\2\u0082\u008c\7v\2\2\u0083\u0084")
        buf.write("\7O\2\2\u0084\u0085\7C\2\2\u0085\u0086\7P\2\2\u0086\u0087")
        buf.write("\7C\2\2\u0087\u0088\7E\2\2\u0088\u0089\7Q\2\2\u0089\u008a")
        buf.write("\7U\2\2\u008a\u008c\7V\2\2\u008bz\3\2\2\2\u008b{\3\2\2")
        buf.write("\2\u008b\u0083\3\2\2\2\u008c\"\3\2\2\2\u008d\u009b\t\5")
        buf.write("\2\2\u008e\u008f\7q\2\2\u008f\u0090\7t\2\2\u0090\u0091")
        buf.write("\7c\2\2\u0091\u0092\7e\2\2\u0092\u0093\7n\2\2\u0093\u009b")
        buf.write("\7g\2\2\u0094\u0095\7Q\2\2\u0095\u0096\7T\2\2\u0096\u0097")
        buf.write("\7C\2\2\u0097\u0098\7E\2\2\u0098\u0099\7N\2\2\u0099\u009b")
        buf.write("\7G\2\2\u009a\u008d\3\2\2\2\u009a\u008e\3\2\2\2\u009a")
        buf.write("\u0094\3\2\2\2\u009b$\3\2\2\2\u009c\u009d\7r\2\2\u009d")
        buf.write("\u009e\7q\2\2\u009e\u009f\7y\2\2\u009f\u00a0\7g\2\2\u00a0")
        buf.write("\u00ab\7t\2\2\u00a1\u00a2\7R\2\2\u00a2\u00a3\7Q\2\2\u00a3")
        buf.write("\u00a4\7Y\2\2\u00a4\u00a5\7G\2\2\u00a5\u00ab\7T\2\2\u00a6")
        buf.write("\u00a7\7r\2\2\u00a7\u00ab\7q\2\2\u00a8\u00a9\7R\2\2\u00a9")
        buf.write("\u00ab\7Q\2\2\u00aa\u009c\3\2\2\2\u00aa\u00a1\3\2\2\2")
        buf.write("\u00aa\u00a6\3\2\2\2\u00aa\u00a8\3\2\2\2\u00ab&\3\2\2")
        buf.write("\2\u00ac\u00c4\t\6\2\2\u00ad\u00ae\7v\2\2\u00ae\u00af")
        buf.write("\7q\2\2\u00af\u00b0\7w\2\2\u00b0\u00b1\7i\2\2\u00b1\u00b2")
        buf.write("\7j\2\2\u00b2\u00b3\7p\2\2\u00b3\u00b4\7g\2\2\u00b4\u00b5")
        buf.write("\7u\2\2\u00b5\u00c4\7u\2\2\u00b6\u00b7\7V\2\2\u00b7\u00b8")
        buf.write("\7Q\2\2\u00b8\u00b9\7W\2\2\u00b9\u00ba\7I\2\2\u00ba\u00bb")
        buf.write("\7J\2\2\u00bb\u00bc\7P\2\2\u00bc\u00bd\7G\2\2\u00bd\u00be")
        buf.write("\7U\2\2\u00be\u00c4\7U\2\2\u00bf\u00c0\7v\2\2\u00c0\u00c4")
        buf.write("\7q\2\2\u00c1\u00c2\7V\2\2\u00c2\u00c4\7Q\2\2\u00c3\u00ac")
        buf.write("\3\2\2\2\u00c3\u00ad\3\2\2\2\u00c3\u00b6\3\2\2\2\u00c3")
        buf.write("\u00bf\3\2\2\2\u00c3\u00c1\3\2\2\2\u00c4(\3\2\2\2\u00c5")
        buf.write("\u00c6\7n\2\2\u00c6\u00c7\7q\2\2\u00c7\u00c8\7{\2\2\u00c8")
        buf.write("\u00c9\7c\2\2\u00c9\u00ca\7n\2\2\u00ca\u00cb\7v\2\2\u00cb")
        buf.write("\u00d4\7{\2\2\u00cc\u00cd\7N\2\2\u00cd\u00ce\7Q\2\2\u00ce")
        buf.write("\u00cf\7[\2\2\u00cf\u00d0\7C\2\2\u00d0\u00d1\7N\2\2\u00d1")
        buf.write("\u00d2\7V\2\2\u00d2\u00d4\7[\2\2\u00d3\u00c5\3\2\2\2\u00d3")
        buf.write("\u00cc\3\2\2\2\u00d4*\3\2\2\2\u00d5\u00d6\7c\2\2\u00d6")
        buf.write("\u00d7\7t\2\2\u00d7\u00d8\7v\2\2\u00d8\u00d9\7k\2\2\u00d9")
        buf.write("\u00da\7u\2\2\u00da\u00e2\7v\2\2\u00db\u00dc\7C\2\2\u00dc")
        buf.write("\u00dd\7T\2\2\u00dd\u00de\7V\2\2\u00de\u00df\7K\2\2\u00df")
        buf.write("\u00e0\7U\2\2\u00e0\u00e2\7V\2\2\u00e1\u00d5\3\2\2\2\u00e1")
        buf.write("\u00db\3\2\2\2\u00e2,\3\2\2\2\u00e3\u00e4\7e\2\2\u00e4")
        buf.write("\u00e5\7o\2\2\u00e5\u00ea\7e\2\2\u00e6\u00e7\7E\2\2\u00e7")
        buf.write("\u00e8\7O\2\2\u00e8\u00ea\7E\2\2\u00e9\u00e3\3\2\2\2\u00e9")
        buf.write("\u00e6\3\2\2\2\u00ea.\3\2\2\2\u00eb\u00ec\7t\2\2\u00ec")
        buf.write("\u00ed\7c\2\2\u00ed\u00ee\7t\2\2\u00ee\u00ef\7k\2\2\u00ef")
        buf.write("\u00f0\7v\2\2\u00f0\u00f8\7{\2\2\u00f1\u00f2\7T\2\2\u00f2")
        buf.write("\u00f3\7C\2\2\u00f3\u00f4\7T\2\2\u00f4\u00f5\7K\2\2\u00f5")
        buf.write("\u00f6\7V\2\2\u00f6\u00f8\7[\2\2\u00f7\u00eb\3\2\2\2\u00f7")
        buf.write("\u00f1\3\2\2\2\u00f8\60\3\2\2\2\u00f9\u00fa\7n\2\2\u00fa")
        buf.write("\u00fb\7c\2\2\u00fb\u00fc\7{\2\2\u00fc\u00fd\7q\2\2\u00fd")
        buf.write("\u00fe\7w\2\2\u00fe\u0106\7v\2\2\u00ff\u0100\7N\2\2\u0100")
        buf.write("\u0101\7C\2\2\u0101\u0102\7[\2\2\u0102\u0103\7Q\2\2\u0103")
        buf.write("\u0104\7W\2\2\u0104\u0106\7V\2\2\u0105\u00f9\3\2\2\2\u0105")
        buf.write("\u00ff\3\2\2\2\u0106\62\3\2\2\2\u0107\u0108\7h\2\2\u0108")
        buf.write("\u0109\7n\2\2\u0109\u010a\7c\2\2\u010a\u010b\7i\2\2\u010b")
        buf.write("\u0112\7u\2\2\u010c\u010d\7H\2\2\u010d\u010e\7N\2\2\u010e")
        buf.write("\u010f\7C\2\2\u010f\u0110\7I\2\2\u0110\u0112\7U\2\2\u0111")
        buf.write("\u0107\3\2\2\2\u0111\u010c\3\2\2\2\u0112\64\3\2\2\2\u0113")
        buf.write("\u0114\7h\2\2\u0114\u0115\7n\2\2\u0115\u0116\7c\2\2\u0116")
        buf.write("\u0117\7x\2\2\u0117\u0118\7q\2\2\u0118\u0120\7t\2\2\u0119")
        buf.write("\u011a\7H\2\2\u011a\u011b\7N\2\2\u011b\u011c\7C\2\2\u011c")
        buf.write("\u011d\7X\2\2\u011d\u011e\7Q\2\2\u011e\u0120\7T\2\2\u011f")
        buf.write("\u0113\3\2\2\2\u011f\u0119\3\2\2\2\u0120\66\3\2\2\2\u0121")
        buf.write("\u0135\t\7\2\2\u0122\u0123\7g\2\2\u0123\u0124\7z\2\2\u0124")
        buf.write("\u0125\7r\2\2\u0125\u0126\7c\2\2\u0126\u0127\7p\2\2\u0127")
        buf.write("\u0128\7u\2\2\u0128\u0129\7k\2\2\u0129\u012a\7q\2\2\u012a")
        buf.write("\u0135\7p\2\2\u012b\u012c\7G\2\2\u012c\u012d\7Z\2\2\u012d")
        buf.write("\u012e\7R\2\2\u012e\u012f\7C\2\2\u012f\u0130\7P\2\2\u0130")
        buf.write("\u0131\7U\2\2\u0131\u0132\7K\2\2\u0132\u0133\7Q\2\2\u0133")
        buf.write("\u0135\7P\2\2\u0134\u0121\3\2\2\2\u0134\u0122\3\2\2\2")
        buf.write("\u0134\u012b\3\2\2\2\u01358\3\2\2\2\u0136\u0137\7d\2\2")
        buf.write("\u0137\u0138\7n\2\2\u0138\u0139\7q\2\2\u0139\u013a\7e")
        buf.write("\2\2\u013a\u0141\7m\2\2\u013b\u013c\7D\2\2\u013c\u013d")
        buf.write("\7N\2\2\u013d\u013e\7Q\2\2\u013e\u013f\7E\2\2\u013f\u0141")
        buf.write("\7M\2\2\u0140\u0136\3\2\2\2\u0140\u013b\3\2\2\2\u0141")
        buf.write(":\3\2\2\2\u0142\u0143\7e\2\2\u0143\u0159\7c\2\2\u0144")
        buf.write("\u0145\7E\2\2\u0145\u0159\7C\2\2\u0146\u0147\7e\2\2\u0147")
        buf.write("\u0148\7c\2\2\u0148\u0149\7t\2\2\u0149\u014a\7f\2\2\u014a")
        buf.write("\u014b\7d\2\2\u014b\u014c\7q\2\2\u014c\u014d\7c\2\2\u014d")
        buf.write("\u014e\7t\2\2\u014e\u0159\7f\2\2\u014f\u0150\7E\2\2\u0150")
        buf.write("\u0151\7C\2\2\u0151\u0152\7T\2\2\u0152\u0153\7F\2\2\u0153")
        buf.write("\u0154\7D\2\2\u0154\u0155\7Q\2\2\u0155\u0156\7C\2\2\u0156")
        buf.write("\u0157\7T\2\2\u0157\u0159\7F\2\2\u0158\u0142\3\2\2\2\u0158")
        buf.write("\u0144\3\2\2\2\u0158\u0146\3\2\2\2\u0158\u014f\3\2\2\2")
        buf.write("\u0159<\3\2\2\2\u015a\u015b\7r\2\2\u015b\u016f\7t\2\2")
        buf.write("\u015c\u015d\7R\2\2\u015d\u016f\7T\2\2\u015e\u015f\7r")
        buf.write("\2\2\u015f\u0160\7t\2\2\u0160\u0161\7k\2\2\u0161\u0162")
        buf.write("\7p\2\2\u0162\u0163\7v\2\2\u0163\u0164\7k\2\2\u0164\u0165")
        buf.write("\7p\2\2\u0165\u016f\7i\2\2\u0166\u0167\7R\2\2\u0167\u0168")
        buf.write("\7T\2\2\u0168\u0169\7K\2\2\u0169\u016a\7P\2\2\u016a\u016b")
        buf.write("\7V\2\2\u016b\u016c\7K\2\2\u016c\u016d\7P\2\2\u016d\u016f")
        buf.write("\7I\2\2\u016e\u015a\3\2\2\2\u016e\u015c\3\2\2\2\u016e")
        buf.write("\u015e\3\2\2\2\u016e\u0166\3\2\2\2\u016f>\3\2\2\2\u0170")
        buf.write("\u0172\t\b\2\2\u0171\u0170\3\2\2\2\u0172\u0173\3\2\2\2")
        buf.write("\u0173\u0171\3\2\2\2\u0173\u0174\3\2\2\2\u0174@\3\2\2")
        buf.write("\2\u0175\u0179\7$\2\2\u0176\u0178\n\t\2\2\u0177\u0176")
        buf.write("\3\2\2\2\u0178\u017b\3\2\2\2\u0179\u0177\3\2\2\2\u0179")
        buf.write("\u017a\3\2\2\2\u017a\u017c\3\2\2\2\u017b\u0179\3\2\2\2")
        buf.write("\u017c\u017d\7$\2\2\u017dB\3\2\2\2\u017e\u0180\t\n\2\2")
        buf.write("\u017f\u017e\3\2\2\2\u0180\u0181\3\2\2\2\u0181\u017f\3")
        buf.write("\2\2\2\u0181\u0182\3\2\2\2\u0182D\3\2\2\2\u0183\u0184")
        buf.write("\t\13\2\2\u0184\u0185\3\2\2\2\u0185\u0186\b#\2\2\u0186")
        buf.write("F\3\2\2\2\27\2mx\u008b\u009a\u00aa\u00c3\u00d3\u00e1\u00e9")
        buf.write("\u00f7\u0105\u0111\u011f\u0134\u0140\u0158\u016e\u0173")
        buf.write("\u0179\u0181\3\b\2\2")
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
    T__11 = 12
    DYNAMIC_VALUE = 13
    NAME_CODE = 14
    TYPE_CODE = 15
    MANA_CODE = 16
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
            "'#'", "'!'", "'('", "')'", "'&'", "'||'", "'='", "';'", "'<'", 
            "'<='", "'>'", "'>='", "'@'" ]

    symbolicNames = [ "<INVALID>",
            "DYNAMIC_VALUE", "NAME_CODE", "TYPE_CODE", "MANA_CODE", "ORACLE_CODE", 
            "POWER_CODE", "TOUGHNESS_CODE", "LOYALTY_CODE", "ARTIST_CODE", 
            "CMC_CODE", "RARITY_CODE", "LAYOUT_CODE", "FLAGS_CODE", "FLAVOR_CODE", 
            "EXPANSION_CODE", "BLOCK_CODE", "CARDBOARD_CODE", "PRINTING_CODE", 
            "UNSIGNED_INTEGER", "QUOTED_VALUE", "VALUE", "WHITESPACE" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "DYNAMIC_VALUE", 
                  "NAME_CODE", "TYPE_CODE", "MANA_CODE", "ORACLE_CODE", 
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


