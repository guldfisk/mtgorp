# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/db/attributeparse/manacost/manacost_grammar.g4 by ANTLR 4.7
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\17")
        buf.write("=\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2")
        buf.write("\3\3\3\3\3\3\3\3\3\3\7\3\25\n\3\f\3\16\3\30\13\3\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4#\n\4\3\5\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5/\n\5\3\6\3\6\3\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\5\6;\n\6\3\6\2\3\4\7\2\4\6\b\n")
        buf.write("\2\2\2F\2\f\3\2\2\2\4\17\3\2\2\2\6\"\3\2\2\2\b.\3\2\2")
        buf.write("\2\n:\3\2\2\2\f\r\5\4\3\2\r\16\7\2\2\3\16\3\3\2\2\2\17")
        buf.write("\20\b\3\1\2\20\21\5\6\4\2\21\26\3\2\2\2\22\23\f\3\2\2")
        buf.write("\23\25\5\6\4\2\24\22\3\2\2\2\25\30\3\2\2\2\26\24\3\2\2")
        buf.write("\2\26\27\3\2\2\2\27\5\3\2\2\2\30\26\3\2\2\2\31#\5\n\6")
        buf.write("\2\32\33\7\3\2\2\33\34\5\6\4\2\34\35\7\4\2\2\35#\3\2\2")
        buf.write("\2\36\37\7\3\2\2\37 \5\b\5\2 !\7\4\2\2!#\3\2\2\2\"\31")
        buf.write("\3\2\2\2\"\32\3\2\2\2\"\36\3\2\2\2#\7\3\2\2\2$/\5\6\4")
        buf.write("\2%/\5\4\3\2&\'\5\6\4\2\'(\7\5\2\2()\5\b\5\2)/\3\2\2\2")
        buf.write("*+\5\4\3\2+,\7\5\2\2,-\5\b\5\2-/\3\2\2\2.$\3\2\2\2.%\3")
        buf.write("\2\2\2.&\3\2\2\2.*\3\2\2\2/\t\3\2\2\2\60;\7\6\2\2\61;")
        buf.write("\7\7\2\2\62;\7\b\2\2\63;\7\t\2\2\64;\7\n\2\2\65;\7\13")
        buf.write("\2\2\66;\7\f\2\2\67;\7\r\2\28;\7\16\2\29;\7\17\2\2:\60")
        buf.write("\3\2\2\2:\61\3\2\2\2:\62\3\2\2\2:\63\3\2\2\2:\64\3\2\2")
        buf.write("\2:\65\3\2\2\2:\66\3\2\2\2:\67\3\2\2\2:8\3\2\2\2:9\3\2")
        buf.write("\2\2;\13\3\2\2\2\6\26\".:")
        return buf.getvalue()


class manacost_grammarParser ( Parser ):

    grammarFileName = "manacost_grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'/'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "WHITE_SYMBOL", "BLUE_SYMBOL", "BLACK_SYMBOL", "RED_SYMBOL", 
                      "GREEN_SYMBOL", "PHYREXIAN_SYMBOL", "SNOW_SYMBOL", 
                      "COLORLESS_SYMBOL", "GENERIC_SYMBOL", "VARIABLE_SYMBOL" ]

    RULE_start = 0
    RULE_mana_cost = 1
    RULE_mana_cost_atom = 2
    RULE_hybrid = 3
    RULE_mana_cost_symbol = 4

    ruleNames =  [ "start", "mana_cost", "mana_cost_atom", "hybrid", "mana_cost_symbol" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    WHITE_SYMBOL=4
    BLUE_SYMBOL=5
    BLACK_SYMBOL=6
    RED_SYMBOL=7
    GREEN_SYMBOL=8
    PHYREXIAN_SYMBOL=9
    SNOW_SYMBOL=10
    COLORLESS_SYMBOL=11
    GENERIC_SYMBOL=12
    VARIABLE_SYMBOL=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class StartContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mana_cost(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_costContext,0)


        def EOF(self):
            return self.getToken(manacost_grammarParser.EOF, 0)

        def getRuleIndex(self):
            return manacost_grammarParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = manacost_grammarParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.mana_cost(0)
            self.state = 11
            self.match(manacost_grammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Mana_costContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return manacost_grammarParser.RULE_mana_cost

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AtomContext(Mana_costContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_costContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost_atom(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_atomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)


    class AtomManaCostContext(Mana_costContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_costContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_costContext,0)

        def mana_cost_atom(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_atomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomManaCost" ):
                listener.enterAtomManaCost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomManaCost" ):
                listener.exitAtomManaCost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomManaCost" ):
                return visitor.visitAtomManaCost(self)
            else:
                return visitor.visitChildren(self)



    def mana_cost(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = manacost_grammarParser.Mana_costContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_mana_cost, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = manacost_grammarParser.AtomContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 14
            self.mana_cost_atom()
            self._ctx.stop = self._input.LT(-1)
            self.state = 20
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = manacost_grammarParser.AtomManaCostContext(self, manacost_grammarParser.Mana_costContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_mana_cost)
                    self.state = 16
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 17
                    self.mana_cost_atom() 
                self.state = 22
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class Mana_cost_atomContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return manacost_grammarParser.RULE_mana_cost_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BracedHybridContext(Mana_cost_atomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_atomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def hybrid(self):
            return self.getTypedRuleContext(manacost_grammarParser.HybridContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBracedHybrid" ):
                listener.enterBracedHybrid(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBracedHybrid" ):
                listener.exitBracedHybrid(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBracedHybrid" ):
                return visitor.visitBracedHybrid(self)
            else:
                return visitor.visitChildren(self)


    class SymbolContext(Mana_cost_atomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_atomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost_symbol(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_symbolContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSymbol" ):
                listener.enterSymbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSymbol" ):
                listener.exitSymbol(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSymbol" ):
                return visitor.visitSymbol(self)
            else:
                return visitor.visitChildren(self)


    class BracedSymbolContext(Mana_cost_atomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_atomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost_atom(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_atomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBracedSymbol" ):
                listener.enterBracedSymbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBracedSymbol" ):
                listener.exitBracedSymbol(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBracedSymbol" ):
                return visitor.visitBracedSymbol(self)
            else:
                return visitor.visitChildren(self)



    def mana_cost_atom(self):

        localctx = manacost_grammarParser.Mana_cost_atomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_mana_cost_atom)
        try:
            self.state = 32
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = manacost_grammarParser.SymbolContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.mana_cost_symbol()
                pass

            elif la_ == 2:
                localctx = manacost_grammarParser.BracedSymbolContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self.match(manacost_grammarParser.T__0)
                self.state = 25
                self.mana_cost_atom()
                self.state = 26
                self.match(manacost_grammarParser.T__1)
                pass

            elif la_ == 3:
                localctx = manacost_grammarParser.BracedHybridContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 28
                self.match(manacost_grammarParser.T__0)
                self.state = 29
                self.hybrid()
                self.state = 30
                self.match(manacost_grammarParser.T__1)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class HybridContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return manacost_grammarParser.RULE_hybrid

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class HybridManaCostContext(HybridContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.HybridContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_costContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHybridManaCost" ):
                listener.enterHybridManaCost(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHybridManaCost" ):
                listener.exitHybridManaCost(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHybridManaCost" ):
                return visitor.visitHybridManaCost(self)
            else:
                return visitor.visitChildren(self)


    class HybridAtomContext(HybridContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.HybridContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost_atom(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_atomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHybridAtom" ):
                listener.enterHybridAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHybridAtom" ):
                listener.exitHybridAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHybridAtom" ):
                return visitor.visitHybridAtom(self)
            else:
                return visitor.visitChildren(self)


    class ManaCostHybridContext(HybridContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.HybridContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_costContext,0)

        def hybrid(self):
            return self.getTypedRuleContext(manacost_grammarParser.HybridContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterManaCostHybrid" ):
                listener.enterManaCostHybrid(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitManaCostHybrid" ):
                listener.exitManaCostHybrid(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitManaCostHybrid" ):
                return visitor.visitManaCostHybrid(self)
            else:
                return visitor.visitChildren(self)


    class AtomHybridContext(HybridContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.HybridContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def mana_cost_atom(self):
            return self.getTypedRuleContext(manacost_grammarParser.Mana_cost_atomContext,0)

        def hybrid(self):
            return self.getTypedRuleContext(manacost_grammarParser.HybridContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomHybrid" ):
                listener.enterAtomHybrid(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomHybrid" ):
                listener.exitAtomHybrid(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomHybrid" ):
                return visitor.visitAtomHybrid(self)
            else:
                return visitor.visitChildren(self)



    def hybrid(self):

        localctx = manacost_grammarParser.HybridContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_hybrid)
        try:
            self.state = 44
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = manacost_grammarParser.HybridAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.mana_cost_atom()
                pass

            elif la_ == 2:
                localctx = manacost_grammarParser.HybridManaCostContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.mana_cost(0)
                pass

            elif la_ == 3:
                localctx = manacost_grammarParser.AtomHybridContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 36
                self.mana_cost_atom()
                self.state = 37
                self.match(manacost_grammarParser.T__2)
                self.state = 38
                self.hybrid()
                pass

            elif la_ == 4:
                localctx = manacost_grammarParser.ManaCostHybridContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 40
                self.mana_cost(0)
                self.state = 41
                self.match(manacost_grammarParser.T__2)
                self.state = 42
                self.hybrid()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Mana_cost_symbolContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return manacost_grammarParser.RULE_mana_cost_symbol

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class RedContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RED_SYMBOL(self):
            return self.getToken(manacost_grammarParser.RED_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRed" ):
                listener.enterRed(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRed" ):
                listener.exitRed(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRed" ):
                return visitor.visitRed(self)
            else:
                return visitor.visitChildren(self)


    class WhiteContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def WHITE_SYMBOL(self):
            return self.getToken(manacost_grammarParser.WHITE_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhite" ):
                listener.enterWhite(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhite" ):
                listener.exitWhite(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhite" ):
                return visitor.visitWhite(self)
            else:
                return visitor.visitChildren(self)


    class ColorlessContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def COLORLESS_SYMBOL(self):
            return self.getToken(manacost_grammarParser.COLORLESS_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterColorless" ):
                listener.enterColorless(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitColorless" ):
                listener.exitColorless(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColorless" ):
                return visitor.visitColorless(self)
            else:
                return visitor.visitChildren(self)


    class VariableContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE_SYMBOL(self):
            return self.getToken(manacost_grammarParser.VARIABLE_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)


    class SnowContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SNOW_SYMBOL(self):
            return self.getToken(manacost_grammarParser.SNOW_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSnow" ):
                listener.enterSnow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSnow" ):
                listener.exitSnow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSnow" ):
                return visitor.visitSnow(self)
            else:
                return visitor.visitChildren(self)


    class BlueContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BLUE_SYMBOL(self):
            return self.getToken(manacost_grammarParser.BLUE_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlue" ):
                listener.enterBlue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlue" ):
                listener.exitBlue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlue" ):
                return visitor.visitBlue(self)
            else:
                return visitor.visitChildren(self)


    class GenericContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def GENERIC_SYMBOL(self):
            return self.getToken(manacost_grammarParser.GENERIC_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGeneric" ):
                listener.enterGeneric(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGeneric" ):
                listener.exitGeneric(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGeneric" ):
                return visitor.visitGeneric(self)
            else:
                return visitor.visitChildren(self)


    class BlackContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BLACK_SYMBOL(self):
            return self.getToken(manacost_grammarParser.BLACK_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlack" ):
                listener.enterBlack(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlack" ):
                listener.exitBlack(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlack" ):
                return visitor.visitBlack(self)
            else:
                return visitor.visitChildren(self)


    class PhyrexianContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PHYREXIAN_SYMBOL(self):
            return self.getToken(manacost_grammarParser.PHYREXIAN_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhyrexian" ):
                listener.enterPhyrexian(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhyrexian" ):
                listener.exitPhyrexian(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhyrexian" ):
                return visitor.visitPhyrexian(self)
            else:
                return visitor.visitChildren(self)


    class GreenContext(Mana_cost_symbolContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a manacost_grammarParser.Mana_cost_symbolContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def GREEN_SYMBOL(self):
            return self.getToken(manacost_grammarParser.GREEN_SYMBOL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGreen" ):
                listener.enterGreen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGreen" ):
                listener.exitGreen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGreen" ):
                return visitor.visitGreen(self)
            else:
                return visitor.visitChildren(self)



    def mana_cost_symbol(self):

        localctx = manacost_grammarParser.Mana_cost_symbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_mana_cost_symbol)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [manacost_grammarParser.WHITE_SYMBOL]:
                localctx = manacost_grammarParser.WhiteContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 46
                self.match(manacost_grammarParser.WHITE_SYMBOL)
                pass
            elif token in [manacost_grammarParser.BLUE_SYMBOL]:
                localctx = manacost_grammarParser.BlueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.match(manacost_grammarParser.BLUE_SYMBOL)
                pass
            elif token in [manacost_grammarParser.BLACK_SYMBOL]:
                localctx = manacost_grammarParser.BlackContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 48
                self.match(manacost_grammarParser.BLACK_SYMBOL)
                pass
            elif token in [manacost_grammarParser.RED_SYMBOL]:
                localctx = manacost_grammarParser.RedContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 49
                self.match(manacost_grammarParser.RED_SYMBOL)
                pass
            elif token in [manacost_grammarParser.GREEN_SYMBOL]:
                localctx = manacost_grammarParser.GreenContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 50
                self.match(manacost_grammarParser.GREEN_SYMBOL)
                pass
            elif token in [manacost_grammarParser.PHYREXIAN_SYMBOL]:
                localctx = manacost_grammarParser.PhyrexianContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 51
                self.match(manacost_grammarParser.PHYREXIAN_SYMBOL)
                pass
            elif token in [manacost_grammarParser.SNOW_SYMBOL]:
                localctx = manacost_grammarParser.SnowContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 52
                self.match(manacost_grammarParser.SNOW_SYMBOL)
                pass
            elif token in [manacost_grammarParser.COLORLESS_SYMBOL]:
                localctx = manacost_grammarParser.ColorlessContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 53
                self.match(manacost_grammarParser.COLORLESS_SYMBOL)
                pass
            elif token in [manacost_grammarParser.GENERIC_SYMBOL]:
                localctx = manacost_grammarParser.GenericContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 54
                self.match(manacost_grammarParser.GENERIC_SYMBOL)
                pass
            elif token in [manacost_grammarParser.VARIABLE_SYMBOL]:
                localctx = manacost_grammarParser.VariableContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 55
                self.match(manacost_grammarParser.VARIABLE_SYMBOL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.mana_cost_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def mana_cost_sempred(self, localctx:Mana_costContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         




