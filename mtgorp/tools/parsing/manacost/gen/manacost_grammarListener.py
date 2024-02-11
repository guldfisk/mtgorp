# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/manacost/manacost_grammar.g4 by ANTLR 4.7
from antlr4 import *


if __name__ is not None and "." in __name__:
    from .manacost_grammarParser import manacost_grammarParser
else:
    from manacost_grammarParser import manacost_grammarParser


# This class defines a complete listener for a parse tree produced by manacost_grammarParser.
class manacost_grammarListener(ParseTreeListener):
    # Enter a parse tree produced by manacost_grammarParser#Empty.
    def enterEmpty(self, ctx: manacost_grammarParser.EmptyContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Empty.
    def exitEmpty(self, ctx: manacost_grammarParser.EmptyContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#NonEmpty.
    def enterNonEmpty(self, ctx: manacost_grammarParser.NonEmptyContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#NonEmpty.
    def exitNonEmpty(self, ctx: manacost_grammarParser.NonEmptyContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Atom.
    def enterAtom(self, ctx: manacost_grammarParser.AtomContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Atom.
    def exitAtom(self, ctx: manacost_grammarParser.AtomContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#AtomManaCost.
    def enterAtomManaCost(self, ctx: manacost_grammarParser.AtomManaCostContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#AtomManaCost.
    def exitAtomManaCost(self, ctx: manacost_grammarParser.AtomManaCostContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Symbol.
    def enterSymbol(self, ctx: manacost_grammarParser.SymbolContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Symbol.
    def exitSymbol(self, ctx: manacost_grammarParser.SymbolContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#BracedSymbol.
    def enterBracedSymbol(self, ctx: manacost_grammarParser.BracedSymbolContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#BracedSymbol.
    def exitBracedSymbol(self, ctx: manacost_grammarParser.BracedSymbolContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#BracedHybrid.
    def enterBracedHybrid(self, ctx: manacost_grammarParser.BracedHybridContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#BracedHybrid.
    def exitBracedHybrid(self, ctx: manacost_grammarParser.BracedHybridContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#HybridAtom.
    def enterHybridAtom(self, ctx: manacost_grammarParser.HybridAtomContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#HybridAtom.
    def exitHybridAtom(self, ctx: manacost_grammarParser.HybridAtomContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#HybridManaCost.
    def enterHybridManaCost(self, ctx: manacost_grammarParser.HybridManaCostContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#HybridManaCost.
    def exitHybridManaCost(self, ctx: manacost_grammarParser.HybridManaCostContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#AtomHybrid.
    def enterAtomHybrid(self, ctx: manacost_grammarParser.AtomHybridContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#AtomHybrid.
    def exitAtomHybrid(self, ctx: manacost_grammarParser.AtomHybridContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#ManaCostHybrid.
    def enterManaCostHybrid(self, ctx: manacost_grammarParser.ManaCostHybridContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#ManaCostHybrid.
    def exitManaCostHybrid(self, ctx: manacost_grammarParser.ManaCostHybridContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#White.
    def enterWhite(self, ctx: manacost_grammarParser.WhiteContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#White.
    def exitWhite(self, ctx: manacost_grammarParser.WhiteContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Blue.
    def enterBlue(self, ctx: manacost_grammarParser.BlueContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Blue.
    def exitBlue(self, ctx: manacost_grammarParser.BlueContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Black.
    def enterBlack(self, ctx: manacost_grammarParser.BlackContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Black.
    def exitBlack(self, ctx: manacost_grammarParser.BlackContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Red.
    def enterRed(self, ctx: manacost_grammarParser.RedContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Red.
    def exitRed(self, ctx: manacost_grammarParser.RedContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Green.
    def enterGreen(self, ctx: manacost_grammarParser.GreenContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Green.
    def exitGreen(self, ctx: manacost_grammarParser.GreenContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Phyrexian.
    def enterPhyrexian(self, ctx: manacost_grammarParser.PhyrexianContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Phyrexian.
    def exitPhyrexian(self, ctx: manacost_grammarParser.PhyrexianContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Snow.
    def enterSnow(self, ctx: manacost_grammarParser.SnowContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Snow.
    def exitSnow(self, ctx: manacost_grammarParser.SnowContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Colorless.
    def enterColorless(self, ctx: manacost_grammarParser.ColorlessContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Colorless.
    def exitColorless(self, ctx: manacost_grammarParser.ColorlessContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Generic.
    def enterGeneric(self, ctx: manacost_grammarParser.GenericContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Generic.
    def exitGeneric(self, ctx: manacost_grammarParser.GenericContext):
        pass

    # Enter a parse tree produced by manacost_grammarParser#Variable.
    def enterVariable(self, ctx: manacost_grammarParser.VariableContext):
        pass

    # Exit a parse tree produced by manacost_grammarParser#Variable.
    def exitVariable(self, ctx: manacost_grammarParser.VariableContext):
        pass
