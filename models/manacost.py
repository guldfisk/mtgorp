from models import colors as c

class ManaCost(object):
	def __init__(self, code, associations, cmc_value=1):
		self.code = code
		self.associations = associations
		self.cmc_value = cmc_value
	def __str__(self):
		return '{'+self.code+'}'
	def __eq__(self, other):
		return issubclass(other, self) and self.code == other.code
	def __hash__(self):
		return hash(self.code)

ONEWHITE = ManaCost('W', frozenset({c.WHITE}))
ONEBLUE = ManaCost('U', frozenset({c.BLUE}))
ONEBLACK = ManaCost('B', frozenset({c.BLACK}))
ONERED = ManaCost('R', frozenset({c.RED}))
ONEGREEN = ManaCost('G', frozenset({c.GREEN}))
ONECOLORLESS = ManaCost('C', frozenset())
ONEVARIABLE = ManaCost('X', frozenset(), 0)

class Generic(ManaCost):
	def __init__(self, amount):
		super(Generic, self).__init__(str(amount), frozenset(), amount)
		self.amount = amount
	def __eq__(self, other):
		return issubclass(other, self) and self.amount == other.amount
	def __hash__(self):
		return hash(self.amount)

class Hybrid(ManaCost):
	def __init__(self, options):
		self.options = frozenset(options)
		self.code = '/'.join(option.code for option in self.options)
		self.associations = frozenset.union(*[option.associations for option in self.options])
		self.cmc_value = max(option.cmc_value for option in self.options)
	def __eq__(self, other):
		return issubclass(other, self) and self.options == other.options
	def __hash__(self):
		return hash(self.options)

class Phyrexian(ManaCost):
	def __init__(self):
		self.code = 'P'
		self.associations = frozenset()
		self.cmc_value = 0

PHYREXIAN = Phyrexian()

ONEWHITEPHYREXIAN = Hybrid({ONEWHITE, PHYREXIAN})