import re

class PowerToughness(object):
	def __init__(self, power: int, toughness: int):
		self._power = power
		self._toughness = toughness
	@property
	def power(self):
		return self._power
	@property
	def toughness(self):
		return self._toughness
	def __eq__(self, other):
		return isinstance(other, PowerToughness) and self.power == other.power and self.toughness == other.toughness
	def __hash__(self):
		return hash((self.power, self.toughness))
	def __repr__(self):
		return '{}/{}'.format(self.power, self.toughness)

class PowerToughnessParseException(Exception): pass

class Parser(object):
	matcher = re.compile('(-?\\d+)/(-?\\d+)')
	@staticmethod
	def parse(s: str) -> PowerToughness:
		m = Parser.matcher.match(s)
		if not m or len(m.groups()) < 2:
			raise PowerToughnessParseException()
		return PowerToughness(int(m.group(1)), int(m.group(2)))

def test():
	pt = PowerToughness(1, 2)
	print(pt)
	opt = Parser.parse('2/2')
	print(opt)
	print(pt == opt)

if __name__ == '__main__':
	test()