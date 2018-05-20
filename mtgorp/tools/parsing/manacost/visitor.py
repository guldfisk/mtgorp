from mtgorp.models.persistent.attributes import manacosts as m

from mtgorp.tools.parsing.manacost.gen.manacost_grammarParser import manacost_grammarParser
from mtgorp.tools.parsing.manacost.gen.manacost_grammarVisitor import manacost_grammarVisitor


class HybridBuilder(list):

	def __repr__(self):
		return f'{self.__class__.__name__}({super().__repr__()})'


class ManaCostBuilder(list):

	def __repr__(self):
		return f'{self.__class__.__name__}({super().__repr__()})'


class ManaCostVisitor(manacost_grammarVisitor):

	def visitStart(self, ctx: manacost_grammarParser.StartContext):
		return self.visit(ctx.mana_cost())

	def visitAtomManaCost(self, ctx:manacost_grammarParser.AtomManaCostContext):
		mana_cost, atom = self.visit(ctx.mana_cost()), self.visit(ctx.mana_cost_atom())
		if isinstance(atom, ManaCostBuilder):
			mana_cost.extend(atom)
		else:
			mana_cost.append(atom)
		return mana_cost

	def visitAtom(self, ctx: manacost_grammarParser.AtomContext):
		atom = self.visit(ctx.mana_cost_atom())
		if isinstance(atom, ManaCostBuilder):
			return atom
		return ManaCostBuilder([atom])

	def visitSymbol(self, ctx: manacost_grammarParser.SymbolContext):
		return self.visit(ctx.mana_cost_symbol())

	def visitBracedSymbol(self, ctx: manacost_grammarParser.BracedSymbolContext):
		return self.visit(ctx.mana_cost_atom())

	def visitBracedHybrid(self, ctx: manacost_grammarParser.BracedHybridContext):
		return self.visit(ctx.hybrid())

	def visitHybridAtom(self, ctx: manacost_grammarParser.HybridAtomContext):
		return HybridBuilder([self.visit(ctx.mana_cost_atom())])

	def visitHybridManaCost(self, ctx:manacost_grammarParser.HybridManaCostContext):
		return HybridBuilder([self.visit(ctx.mana_cost())])

	def visitAtomHybrid(self, ctx: manacost_grammarParser.AtomHybridContext):
		atom, hybrid = self.visit(ctx.mana_cost_atom()), self.visit(ctx.hybrid())
		hybrid.append(atom)
		return hybrid

	def visitManaCostHybrid(self, ctx:manacost_grammarParser.ManaCostHybridContext):
		mana_cost, hybrid = self.visit(ctx.mana_cost()), self.visit(ctx.hybrid())
		hybrid.append(mana_cost)
		return hybrid

	def visitWhite(self, ctx: manacost_grammarParser.WhiteContext):
		return m.ONE_WHITE

	def visitBlue(self, ctx: manacost_grammarParser.BlueContext):
		return m.ONE_BLUE

	def visitBlack(self, ctx: manacost_grammarParser.BlackContext):
		return m.ONE_BLACK

	def visitRed(self, ctx: manacost_grammarParser.RedContext):
		return m.ONE_RED

	def visitGreen(self, ctx: manacost_grammarParser.GreenContext):
		return m.ONE_GREEN

	def visitPhyrexian(self, ctx: manacost_grammarParser.PhyrexianContext):
		return m.ONE_PHYREXIAN

	def visitSnow(self, ctx: manacost_grammarParser.SnowContext):
		return m.ONE_SNOW

	def visitColorless(self, ctx: manacost_grammarParser.ColorlessContext):
		return m.ONE_COLORLESS

	def visitGeneric(self, ctx: manacost_grammarParser.GenericContext):
		return ManaCostBuilder([m.ONE_GENERIC]*int(str(ctx.GENERIC_SYMBOL())))

	def visitVariable(self, ctx: manacost_grammarParser.VariableContext):
		return m.VARIABLE_GENERIC