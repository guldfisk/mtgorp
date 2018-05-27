# Generated from /home/biggenerals/PycharmProjects/mtgorp/mtgorp/tools/parsing/search/search_grammar.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .search_grammarParser import search_grammarParser
else:
    from search_grammarParser import search_grammarParser

# This class defines a complete listener for a parse tree produced by search_grammarParser.
class search_grammarListener(ParseTreeListener):

    # Enter a parse tree produced by search_grammarParser#start.
    def enterStart(self, ctx:search_grammarParser.StartContext):
        pass

    # Exit a parse tree produced by search_grammarParser#start.
    def exitStart(self, ctx:search_grammarParser.StartContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DefaultPattern.
    def enterDefaultPattern(self, ctx:search_grammarParser.DefaultPatternContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DefaultPattern.
    def exitDefaultPattern(self, ctx:search_grammarParser.DefaultPatternContext):
        pass


    # Enter a parse tree produced by search_grammarParser#MatchTypePattern.
    def enterMatchTypePattern(self, ctx:search_grammarParser.MatchTypePatternContext):
        pass

    # Exit a parse tree produced by search_grammarParser#MatchTypePattern.
    def exitMatchTypePattern(self, ctx:search_grammarParser.MatchTypePatternContext):
        pass


    # Enter a parse tree produced by search_grammarParser#CardboardCode.
    def enterCardboardCode(self, ctx:search_grammarParser.CardboardCodeContext):
        pass

    # Exit a parse tree produced by search_grammarParser#CardboardCode.
    def exitCardboardCode(self, ctx:search_grammarParser.CardboardCodeContext):
        pass


    # Enter a parse tree produced by search_grammarParser#PrintingCode.
    def enterPrintingCode(self, ctx:search_grammarParser.PrintingCodeContext):
        pass

    # Exit a parse tree produced by search_grammarParser#PrintingCode.
    def exitPrintingCode(self, ctx:search_grammarParser.PrintingCodeContext):
        pass


    # Enter a parse tree produced by search_grammarParser#Not.
    def enterNot(self, ctx:search_grammarParser.NotContext):
        pass

    # Exit a parse tree produced by search_grammarParser#Not.
    def exitNot(self, ctx:search_grammarParser.NotContext):
        pass


    # Enter a parse tree produced by search_grammarParser#Parenthesis.
    def enterParenthesis(self, ctx:search_grammarParser.ParenthesisContext):
        pass

    # Exit a parse tree produced by search_grammarParser#Parenthesis.
    def exitParenthesis(self, ctx:search_grammarParser.ParenthesisContext):
        pass


    # Enter a parse tree produced by search_grammarParser#RestrictionOperation.
    def enterRestrictionOperation(self, ctx:search_grammarParser.RestrictionOperationContext):
        pass

    # Exit a parse tree produced by search_grammarParser#RestrictionOperation.
    def exitRestrictionOperation(self, ctx:search_grammarParser.RestrictionOperationContext):
        pass


    # Enter a parse tree produced by search_grammarParser#Or.
    def enterOr(self, ctx:search_grammarParser.OrContext):
        pass

    # Exit a parse tree produced by search_grammarParser#Or.
    def exitOr(self, ctx:search_grammarParser.OrContext):
        pass


    # Enter a parse tree produced by search_grammarParser#And.
    def enterAnd(self, ctx:search_grammarParser.AndContext):
        pass

    # Exit a parse tree produced by search_grammarParser#And.
    def exitAnd(self, ctx:search_grammarParser.AndContext):
        pass


    # Enter a parse tree produced by search_grammarParser#NameRestriction.
    def enterNameRestriction(self, ctx:search_grammarParser.NameRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#NameRestriction.
    def exitNameRestriction(self, ctx:search_grammarParser.NameRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#TypeRestriction.
    def enterTypeRestriction(self, ctx:search_grammarParser.TypeRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#TypeRestriction.
    def exitTypeRestriction(self, ctx:search_grammarParser.TypeRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ManaRestriction.
    def enterManaRestriction(self, ctx:search_grammarParser.ManaRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ManaRestriction.
    def exitManaRestriction(self, ctx:search_grammarParser.ManaRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#OracleRestriction.
    def enterOracleRestriction(self, ctx:search_grammarParser.OracleRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#OracleRestriction.
    def exitOracleRestriction(self, ctx:search_grammarParser.OracleRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#PowerRestriction.
    def enterPowerRestriction(self, ctx:search_grammarParser.PowerRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#PowerRestriction.
    def exitPowerRestriction(self, ctx:search_grammarParser.PowerRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ToughnessRestriction.
    def enterToughnessRestriction(self, ctx:search_grammarParser.ToughnessRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ToughnessRestriction.
    def exitToughnessRestriction(self, ctx:search_grammarParser.ToughnessRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#LoyaltyRestriction.
    def enterLoyaltyRestriction(self, ctx:search_grammarParser.LoyaltyRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#LoyaltyRestriction.
    def exitLoyaltyRestriction(self, ctx:search_grammarParser.LoyaltyRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ArtistRestriction.
    def enterArtistRestriction(self, ctx:search_grammarParser.ArtistRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ArtistRestriction.
    def exitArtistRestriction(self, ctx:search_grammarParser.ArtistRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#CmcRestriction.
    def enterCmcRestriction(self, ctx:search_grammarParser.CmcRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#CmcRestriction.
    def exitCmcRestriction(self, ctx:search_grammarParser.CmcRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#RarityRestriction.
    def enterRarityRestriction(self, ctx:search_grammarParser.RarityRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#RarityRestriction.
    def exitRarityRestriction(self, ctx:search_grammarParser.RarityRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#LayoutRestriction.
    def enterLayoutRestriction(self, ctx:search_grammarParser.LayoutRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#LayoutRestriction.
    def exitLayoutRestriction(self, ctx:search_grammarParser.LayoutRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#FlagsRestriction.
    def enterFlagsRestriction(self, ctx:search_grammarParser.FlagsRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#FlagsRestriction.
    def exitFlagsRestriction(self, ctx:search_grammarParser.FlagsRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ExpansionRestriction.
    def enterExpansionRestriction(self, ctx:search_grammarParser.ExpansionRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ExpansionRestriction.
    def exitExpansionRestriction(self, ctx:search_grammarParser.ExpansionRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#BlockRestriction.
    def enterBlockRestriction(self, ctx:search_grammarParser.BlockRestrictionContext):
        pass

    # Exit a parse tree produced by search_grammarParser#BlockRestriction.
    def exitBlockRestriction(self, ctx:search_grammarParser.BlockRestrictionContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ChainValue.
    def enterChainValue(self, ctx:search_grammarParser.ChainValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ChainValue.
    def exitChainValue(self, ctx:search_grammarParser.ChainValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#ChainChain.
    def enterChainChain(self, ctx:search_grammarParser.ChainChainContext):
        pass

    # Exit a parse tree produced by search_grammarParser#ChainChain.
    def exitChainChain(self, ctx:search_grammarParser.ChainChainContext):
        pass


    # Enter a parse tree produced by search_grammarParser#StaticValue.
    def enterStaticValue(self, ctx:search_grammarParser.StaticValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#StaticValue.
    def exitStaticValue(self, ctx:search_grammarParser.StaticValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicValue.
    def enterDynamicValue(self, ctx:search_grammarParser.DynamicValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicValue.
    def exitDynamicValue(self, ctx:search_grammarParser.DynamicValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#InferredValue.
    def enterInferredValue(self, ctx:search_grammarParser.InferredValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#InferredValue.
    def exitInferredValue(self, ctx:search_grammarParser.InferredValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#QuotedValue.
    def enterQuotedValue(self, ctx:search_grammarParser.QuotedValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#QuotedValue.
    def exitQuotedValue(self, ctx:search_grammarParser.QuotedValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#UnsignedIntegerValue.
    def enterUnsignedIntegerValue(self, ctx:search_grammarParser.UnsignedIntegerValueContext):
        pass

    # Exit a parse tree produced by search_grammarParser#UnsignedIntegerValue.
    def exitUnsignedIntegerValue(self, ctx:search_grammarParser.UnsignedIntegerValueContext):
        pass


    # Enter a parse tree produced by search_grammarParser#IncludesOperator.
    def enterIncludesOperator(self, ctx:search_grammarParser.IncludesOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#IncludesOperator.
    def exitIncludesOperator(self, ctx:search_grammarParser.IncludesOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#EqualsOperator.
    def enterEqualsOperator(self, ctx:search_grammarParser.EqualsOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#EqualsOperator.
    def exitEqualsOperator(self, ctx:search_grammarParser.EqualsOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#LessThanOperator.
    def enterLessThanOperator(self, ctx:search_grammarParser.LessThanOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#LessThanOperator.
    def exitLessThanOperator(self, ctx:search_grammarParser.LessThanOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#LessEqualOperator.
    def enterLessEqualOperator(self, ctx:search_grammarParser.LessEqualOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#LessEqualOperator.
    def exitLessEqualOperator(self, ctx:search_grammarParser.LessEqualOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#GreaterThanOperator.
    def enterGreaterThanOperator(self, ctx:search_grammarParser.GreaterThanOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#GreaterThanOperator.
    def exitGreaterThanOperator(self, ctx:search_grammarParser.GreaterThanOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#GreaterEqualOperator.
    def enterGreaterEqualOperator(self, ctx:search_grammarParser.GreaterEqualOperatorContext):
        pass

    # Exit a parse tree produced by search_grammarParser#GreaterEqualOperator.
    def exitGreaterEqualOperator(self, ctx:search_grammarParser.GreaterEqualOperatorContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicName.
    def enterDynamicName(self, ctx:search_grammarParser.DynamicNameContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicName.
    def exitDynamicName(self, ctx:search_grammarParser.DynamicNameContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicOracle.
    def enterDynamicOracle(self, ctx:search_grammarParser.DynamicOracleContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicOracle.
    def exitDynamicOracle(self, ctx:search_grammarParser.DynamicOracleContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicPower.
    def enterDynamicPower(self, ctx:search_grammarParser.DynamicPowerContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicPower.
    def exitDynamicPower(self, ctx:search_grammarParser.DynamicPowerContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicToughness.
    def enterDynamicToughness(self, ctx:search_grammarParser.DynamicToughnessContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicToughness.
    def exitDynamicToughness(self, ctx:search_grammarParser.DynamicToughnessContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicLoyalty.
    def enterDynamicLoyalty(self, ctx:search_grammarParser.DynamicLoyaltyContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicLoyalty.
    def exitDynamicLoyalty(self, ctx:search_grammarParser.DynamicLoyaltyContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicArtist.
    def enterDynamicArtist(self, ctx:search_grammarParser.DynamicArtistContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicArtist.
    def exitDynamicArtist(self, ctx:search_grammarParser.DynamicArtistContext):
        pass


    # Enter a parse tree produced by search_grammarParser#DynamicCmc.
    def enterDynamicCmc(self, ctx:search_grammarParser.DynamicCmcContext):
        pass

    # Exit a parse tree produced by search_grammarParser#DynamicCmc.
    def exitDynamicCmc(self, ctx:search_grammarParser.DynamicCmcContext):
        pass


