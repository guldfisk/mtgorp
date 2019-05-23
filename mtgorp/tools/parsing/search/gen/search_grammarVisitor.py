# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/search/search_grammar.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .search_grammarParser import search_grammarParser
else:
    from search_grammarParser import search_grammarParser

# This class defines a complete generic visitor for a parse tree produced by search_grammarParser.

class search_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by search_grammarParser#start.
    def visitStart(self, ctx:search_grammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#Not.
    def visitNot(self, ctx:search_grammarParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#Parenthesis.
    def visitParenthesis(self, ctx:search_grammarParser.ParenthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#RestrictionOperation.
    def visitRestrictionOperation(self, ctx:search_grammarParser.RestrictionOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#Or.
    def visitOr(self, ctx:search_grammarParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#And.
    def visitAnd(self, ctx:search_grammarParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#NameRestriction.
    def visitNameRestriction(self, ctx:search_grammarParser.NameRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#TypeRestriction.
    def visitTypeRestriction(self, ctx:search_grammarParser.TypeRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ManaRestriction.
    def visitManaRestriction(self, ctx:search_grammarParser.ManaRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ColorRestriction.
    def visitColorRestriction(self, ctx:search_grammarParser.ColorRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#OracleRestriction.
    def visitOracleRestriction(self, ctx:search_grammarParser.OracleRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#PowerRestriction.
    def visitPowerRestriction(self, ctx:search_grammarParser.PowerRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ToughnessRestriction.
    def visitToughnessRestriction(self, ctx:search_grammarParser.ToughnessRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#LoyaltyRestriction.
    def visitLoyaltyRestriction(self, ctx:search_grammarParser.LoyaltyRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ArtistRestriction.
    def visitArtistRestriction(self, ctx:search_grammarParser.ArtistRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#CmcRestriction.
    def visitCmcRestriction(self, ctx:search_grammarParser.CmcRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#RarityRestriction.
    def visitRarityRestriction(self, ctx:search_grammarParser.RarityRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#LayoutRestriction.
    def visitLayoutRestriction(self, ctx:search_grammarParser.LayoutRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#FlagsRestriction.
    def visitFlagsRestriction(self, ctx:search_grammarParser.FlagsRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ExpansionRestriction.
    def visitExpansionRestriction(self, ctx:search_grammarParser.ExpansionRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#BlockRestriction.
    def visitBlockRestriction(self, ctx:search_grammarParser.BlockRestrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ChainValue.
    def visitChainValue(self, ctx:search_grammarParser.ChainValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#ChainChain.
    def visitChainChain(self, ctx:search_grammarParser.ChainChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#StaticValue.
    def visitStaticValue(self, ctx:search_grammarParser.StaticValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicValue.
    def visitDynamicValue(self, ctx:search_grammarParser.DynamicValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#InferredValue.
    def visitInferredValue(self, ctx:search_grammarParser.InferredValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#QuotedValue.
    def visitQuotedValue(self, ctx:search_grammarParser.QuotedValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#UnsignedIntegerValue.
    def visitUnsignedIntegerValue(self, ctx:search_grammarParser.UnsignedIntegerValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#IncludesOperator.
    def visitIncludesOperator(self, ctx:search_grammarParser.IncludesOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#EqualsOperator.
    def visitEqualsOperator(self, ctx:search_grammarParser.EqualsOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#LessThanOperator.
    def visitLessThanOperator(self, ctx:search_grammarParser.LessThanOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#LessEqualOperator.
    def visitLessEqualOperator(self, ctx:search_grammarParser.LessEqualOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#GreaterThanOperator.
    def visitGreaterThanOperator(self, ctx:search_grammarParser.GreaterThanOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#GreaterEqualOperator.
    def visitGreaterEqualOperator(self, ctx:search_grammarParser.GreaterEqualOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicName.
    def visitDynamicName(self, ctx:search_grammarParser.DynamicNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicOracle.
    def visitDynamicOracle(self, ctx:search_grammarParser.DynamicOracleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicPower.
    def visitDynamicPower(self, ctx:search_grammarParser.DynamicPowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicToughness.
    def visitDynamicToughness(self, ctx:search_grammarParser.DynamicToughnessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicLoyalty.
    def visitDynamicLoyalty(self, ctx:search_grammarParser.DynamicLoyaltyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicArtist.
    def visitDynamicArtist(self, ctx:search_grammarParser.DynamicArtistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by search_grammarParser#DynamicCmc.
    def visitDynamicCmc(self, ctx:search_grammarParser.DynamicCmcContext):
        return self.visitChildren(ctx)



del search_grammarParser