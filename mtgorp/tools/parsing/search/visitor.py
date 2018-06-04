from enum import Enum

from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.attributes.powertoughness import PTValue
from mtgorp.tools.search import pattern as p
from mtgorp.tools.parsing.manacost.parse import ManaCostParser
from mtgorp.tools.parsing.search.attributeparse.typeline import TypeLineParser
from mtgorp.tools.parsing.search.attributeparse.ptvalue import PTValueParser
from mtgorp.tools.parsing.search.attributeparse.flags import FlagParser
from mtgorp.tools.parsing.search.attributeparse.rarity import RarityParser
from mtgorp.tools.parsing.search.attributeparse.layout import LayoutParser
from mtgorp.tools.parsing.search.attributeparse.expansion import ExpansionParser
from mtgorp.tools.parsing.search.attributeparse.block import BlockParser

from mtgorp.tools.parsing.search.gen.search_grammarParser import search_grammarParser
from mtgorp.tools.parsing.search.gen.search_grammarVisitor import search_grammarVisitor

from mtgorp.tools.parsing.exceptions import ParseException


class TypeParseException(ParseException):
	pass


class PatternTarget(Enum):
	CARDBOARD = 0
	PRINTING = 1


class SearchPatternBuilder(list):

	def __repr__(self):
		return f'{self.__class__.__name__}({super().__repr__()})'


class AllBuilder(SearchPatternBuilder):
	pass


class AnyBuilder(SearchPatternBuilder):
	pass


class _Chain(list):
	pass


class SearchVisitor(search_grammarVisitor):

	def __init__(self, db: CardDatabase):
		self._target = PatternTarget.CARDBOARD #type: PatternTarget
		self._mana_cost_parser = ManaCostParser()
		self._expansion_parser = ExpansionParser(db)
		self._block_parser = BlockParser(db)

	def visitStart(self, ctx: search_grammarParser.StartContext):
		pattern = self.visit(ctx.pattern())
		if not isinstance(pattern, SearchPatternBuilder):
			return AllBuilder([pattern]), self._target
		return pattern, self._target

	def visitDefaultPattern(self, ctx: search_grammarParser.DefaultPatternContext):
		return self.visit(ctx.operation())

	def visitMatchTypePattern(self, ctx: search_grammarParser.MatchTypePatternContext):
		self.visit(ctx.match_type())
		return self.visit(ctx.operation())

	def visitCardboardCode(self, ctx: search_grammarParser.CardboardCodeContext):
		self._target = PatternTarget.CARDBOARD

	def visitPrintingCode(self, ctx: search_grammarParser.PrintingCodeContext):
		self._target = PatternTarget.PRINTING

	def visitNot(self, ctx: search_grammarParser.NotContext):
		return p.Not(self.visit(ctx.operation()))

	def visitRestrictionOperation(self, ctx: search_grammarParser.RestrictionOperationContext):
		return self.visit(ctx.restriction())

	def visitOr(self, ctx: search_grammarParser.OrContext):
		return AnyBuilder([self.visit(ctx.operation(0)), self.visit(ctx.operation(1))])

	def visitParenthesis(self, ctx: search_grammarParser.ParenthesisContext):
		return self.visit(ctx.operation())

	def visitAnd(self, ctx: search_grammarParser.AndContext):
		return AllBuilder([self.visit(ctx.operation(0)), self.visit(ctx.operation(1))])

	def visitNameRestriction(self, ctx: search_grammarParser.NameRestrictionContext):
		value = self.visit(ctx.value())
		if issubclass(value, p.Extractor) and not value.extraction_type == str:
			raise TypeParseException('Mismatched dynamic value type')
		return (
			(
				p.Contains
				if ctx.operator() is None else
				self.visit(ctx.operator())
			)
			(
				(
					p.CardboardNameExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingNameExtractor
				),
				value if issubclass(value, p.Extractor) else value.lower()
			)
		)

	def visitTypeRestriction(self, ctx: search_grammarParser.TypeRestrictionContext):
		return (
			(
				self.visit(ctx.operator())
			)
				(
				(
					p.CardboardTypesExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingTypesExtractor
				),
				TypeLineParser.parse(self.visit(ctx.value_chain()))
			)
		)

	def visitManaRestriction(self, ctx: search_grammarParser.ManaRestrictionContext):
		return (
			(
				self.visit(ctx.operator())
			)
				(
				(
					p.CardboardManaCostExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingManaCostExtractor
				),
				self._mana_cost_parser.parse(self.visit(ctx.static_value()))
			)
		)

	def visitOracleRestriction(self, ctx: search_grammarParser.OracleRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = value.lower()

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardOracleExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingOracleExtractor
				),
				value,
			)
		)

	def visitPowerRestriction(self, ctx: search_grammarParser.PowerRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type in (int, PTValue):
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = PTValueParser.parse(value)

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardPowerExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingPowerExtractor
				),
				value
			)
		)

	def visitToughnessRestriction(self, ctx: search_grammarParser.ToughnessRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type in (int, PTValue):
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = PTValueParser.parse(value)

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardToughnessExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingToughnessExtractor
				),
				value
			)
		)

	def visitLoyaltyRestriction(self, ctx: search_grammarParser.LoyaltyRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type in (int, PTValue):
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = PTValueParser.parse(value)

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardLoyaltyExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingLoyaltyExtractor
				),
				value
			)
		)

	def visitArtistRestriction(self, ctx: search_grammarParser.ArtistRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = value.lower()

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardArtistExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingArtistExtractor
				),
				value
			)
		)

	def visitCmcRestriction(self, ctx: search_grammarParser.CmcRestrictionContext):
		if ctx.UNSIGNED_INTEGER() is None:
			value = self.visit(ctx.dynamic_value())
			if not value.extraction_type in (int, PTValue):
				raise TypeParseException('Mismatched dynamic value type')
		else:
			value = int(str(ctx.UNSIGNED_INTEGER()))

		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardCMCExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingCMCExtractor
				),
				value
			)
		)

	def visitFlagsRestriction(self, ctx: search_grammarParser.FlagsRestrictionContext):
		return (
			(
				self.visit(ctx.operator())
			)(
				(
					p.CardboardFlagsExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingFlagsExtractor
				),
				FlagParser.parse(self.visit(ctx.value_chain()))
			)
		)

	def visitRarityRestriction(self, ctx: search_grammarParser.RarityRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')

		return (
			(
				p.Equals
			)(
				(
					p.CardboardRarityExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingRarityExtractor
				),
				RarityParser.parse(value)
			)
		)

	def visitLayoutRestriction(self, ctx: search_grammarParser.LayoutRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')

		return (
			(
				p.Equals
			)(
				(
					p.CardboardLayoutExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingLayoutExtractor
				),
				LayoutParser.parse(value)
			)
		)

	def visitExpansionRestriction(self, ctx: search_grammarParser.ExpansionRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')

		return (
			(
				p.Equals
			)(
				(
					p.CardboardExpansionExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingExpansionExtractor
				),
				self._expansion_parser.parse(value)
			)
		)

	def visitBlockRestriction(self, ctx: search_grammarParser.BlockRestrictionContext):
		value = self.visit(ctx.value())

		if isinstance(value, type) and issubclass(value, p.Extractor):
			if not value.extraction_type == str:
				raise TypeParseException('Mismatched dynamic value type')

		return (
			(
				p.Equals
			)(
				(
					p.CardboardBlockExtractor
					if self._target == PatternTarget.CARDBOARD else
					p.PrintingBlockExtractor
				),
				self._block_parser.parse(value)
			)
		)

	def visitStaticValue(self, ctx: search_grammarParser.StaticValueContext):
		return self.visit(ctx.static_value())

	def visitChainValue(self, ctx: search_grammarParser.ChainValueContext):
		return _Chain([self.visit(ctx.static_value())])

	def visitChainChain(self, ctx: search_grammarParser.ChainChainContext):
		chain, value = self.visit(ctx.value_chain()), self.visit(ctx.value())
		chain.append(value)
		return chain

	def visitInferredValue(self, ctx: search_grammarParser.InferredValueContext):
			return ctx.getText()

	def visitQuotedValue(self, ctx: search_grammarParser.QuotedValueContext):
		return ctx.getText()[1:-1]

	def visitDynamicValue(self, ctx: search_grammarParser.DynamicValueContext):
		return self.visit(ctx.dynamic_value())

	def visitUnsignedIntegerValue(self, ctx: search_grammarParser.UnsignedIntegerValueContext):
		return ctx.getText()

	def visitIncludesOperator(self, ctx: search_grammarParser.IncludesOperatorContext):
		return p.Contains

	def visitEqualsOperator(self, ctx: search_grammarParser.EqualsOperatorContext):
		return p.Equals

	def visitLessThanOperator(self, ctx: search_grammarParser.LessThanOperatorContext):
		return p.LessThan

	def visitLessEqualOperator(self, ctx: search_grammarParser.LessEqualOperatorContext):
		return p.LessThanOrEquals

	def visitGreaterThanOperator(self, ctx: search_grammarParser.GreaterThanOperatorContext):
		return p.GreaterThan

	def visitGreaterEqualOperator(self, ctx: search_grammarParser.GreaterEqualOperatorContext):
		return p.GreaterThanOrEquals

	def visitDynamicName(self, ctx: search_grammarParser.DynamicNameContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardNameExtractor
		return p.PrintingNameExtractor

	def visitDynamicOracle(self, ctx: search_grammarParser.DynamicOracleContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardOracleExtractor
		return p.PrintingOracleExtractor

	def visitDynamicPower(self, ctx: search_grammarParser.DynamicPowerContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardPowerExtractor
		return p.PrintingPowerExtractor

	def visitDynamicToughness(self, ctx: search_grammarParser.DynamicToughnessContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardToughnessExtractor
		return p.PrintingToughnessExtractor

	def visitDynamicLoyalty(self, ctx: search_grammarParser.DynamicLoyaltyContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardLoyaltyExtractor
		return p.PrintingFlagsExtractor

	def visitDynamicArtist(self, ctx: search_grammarParser.DynamicArtistContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardArtistExtractor
		return p.PrintingArtistExtractor

	def visitDynamicCmc(self, ctx: search_grammarParser.DynamicCmcContext):
		if self._target == PatternTarget.CARDBOARD:
			return p.CardboardCMCExtractor
		return p.PrintingCMCExtractor