# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/manacost/manacost_grammar.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .manacost_grammarParser import manacost_grammarParser
else:
    from manacost_grammarParser import manacost_grammarParser

# This class defines a complete generic visitor for a parse tree produced by manacost_grammarParser.

class manacost_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by manacost_grammarParser#Empty.
    def visitEmpty(self, ctx:manacost_grammarParser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#NonEmpty.
    def visitNonEmpty(self, ctx:manacost_grammarParser.NonEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Atom.
    def visitAtom(self, ctx:manacost_grammarParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#AtomManaCost.
    def visitAtomManaCost(self, ctx:manacost_grammarParser.AtomManaCostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Symbol.
    def visitSymbol(self, ctx:manacost_grammarParser.SymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#BracedSymbol.
    def visitBracedSymbol(self, ctx:manacost_grammarParser.BracedSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#BracedHybrid.
    def visitBracedHybrid(self, ctx:manacost_grammarParser.BracedHybridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#HybridAtom.
    def visitHybridAtom(self, ctx:manacost_grammarParser.HybridAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#HybridManaCost.
    def visitHybridManaCost(self, ctx:manacost_grammarParser.HybridManaCostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#AtomHybrid.
    def visitAtomHybrid(self, ctx:manacost_grammarParser.AtomHybridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#ManaCostHybrid.
    def visitManaCostHybrid(self, ctx:manacost_grammarParser.ManaCostHybridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#White.
    def visitWhite(self, ctx:manacost_grammarParser.WhiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Blue.
    def visitBlue(self, ctx:manacost_grammarParser.BlueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Black.
    def visitBlack(self, ctx:manacost_grammarParser.BlackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Red.
    def visitRed(self, ctx:manacost_grammarParser.RedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Green.
    def visitGreen(self, ctx:manacost_grammarParser.GreenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Phyrexian.
    def visitPhyrexian(self, ctx:manacost_grammarParser.PhyrexianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Snow.
    def visitSnow(self, ctx:manacost_grammarParser.SnowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Colorless.
    def visitColorless(self, ctx:manacost_grammarParser.ColorlessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Generic.
    def visitGeneric(self, ctx:manacost_grammarParser.GenericContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by manacost_grammarParser#Variable.
    def visitVariable(self, ctx:manacost_grammarParser.VariableContext):
        return self.visitChildren(ctx)



del manacost_grammarParser