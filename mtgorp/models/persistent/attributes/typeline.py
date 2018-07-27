import typing as t

import itertools
import inspect
import sys
from abc import ABCMeta

from lazy_property import LazyProperty


class BaseCardType(metaclass=ABCMeta):

	def __init__(self, name: str):
		self._name = name

	@property
	def name(self):
		return self._name

	def __hash__(self):
		return hash((self.__class__, self._name))

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._name == other.name

	def __repr__(self):
		return self._name

	def __lt__(self, other):
		return self._name < other.name


class CardSuperType(BaseCardType):

	def __lt__(self, other):
		return _SUPER_TYPE_INDEX.get(self, -1) < _SUPER_TYPE_INDEX.get(other, -1)


class CardType(BaseCardType):

	def __init__(self, name: str):
		super().__init__(name)
		self.sub_types = frozenset() #type: t.AbstractSet[CardSubType]

	def __lt__(self, other):
		return _CARD_TYPE_INDEX.get(self, -1) < _CARD_TYPE_INDEX.get(other, -1)

	def __reduce__(self):
		return (
			self.__class__,
			(self._name,),
			{'sub_types': self.sub_types},
		)


class CardSubType(BaseCardType):

	def __init__(self, name: str, card_types: t.Optional[t.Iterable[CardType]] = None):
		super().__init__(name)

		if card_types is None:
			self.card_types = frozenset()
			return

		self.card_types = frozenset(card_types) #type: t.AbstractSet[CardType]

		for card_type in card_types:
			card_type.sub_types |=  frozenset((self,))

	def __reduce__(self):
		return (
			self.__class__,
			(self._name,),
			{'card_types': self.card_types},
		)


class BasicLandType(CardSubType):
	pass


SNOW = CardSuperType('Snow')
LEGENDARY = CardSuperType('Legendary')
WORLD = CardSuperType('World')
BASIC = CardSuperType('Basic')

SUPER_TYPES = (
	LEGENDARY,
	BASIC,
	WORLD,
	SNOW,
)

CREATURE = CardType('Creature')
ARTIFACT = CardType('Artifact')
ENCHANTMENT = CardType('Enchantment')
LAND = CardType('Land')
PLANESWALKER = CardType('Planeswalker')
INSTANT = CardType('Instant')
SORCERY = CardType('Sorcery')
TRIBAL = CardType('Tribal')

CARD_TYPES = (
	TRIBAL,
	ENCHANTMENT,
	ARTIFACT,
	LAND,
	CREATURE,
	PLANESWALKER,
	INSTANT,
	SORCERY
)

_SUPER_TYPE_INDEX = {
	t: idx for idx, t in enumerate(SUPER_TYPES)
}

_CARD_TYPE_INDEX = {
	t: idx for idx, t in enumerate(CARD_TYPES)
}

CLUE = CardSubType('Clue', (ARTIFACT,))
CONTRAPTION = CardSubType('Contraption', (ARTIFACT,))
EQUIPMENT  = CardSubType('Equipment', (ARTIFACT,))
FORTIFICATION  = CardSubType('Fortification', (ARTIFACT,))
TREASURE = CardSubType('Treasure', (ARTIFACT,))
VEHICLE = CardSubType('Vehicle', (ARTIFACT,))

AURA = CardSubType('Aura', (ENCHANTMENT,))
CARTOUCHE = CardSubType('Cartouche', (ENCHANTMENT,))
CURSE = CardSubType('Curse', (ENCHANTMENT,))
SAGA = CardSubType('Saga', (ENCHANTMENT,))
SHRINE = CardSubType('Shrine', (ENCHANTMENT,))

DESERT = CardSubType('Desert', (LAND,))
FOREST = BasicLandType('Forest', (LAND,))
GATE = CardSubType('Gate', (LAND,))
ISLAND = BasicLandType('Island', (LAND,))
LAIR = CardSubType('Lair', (LAND,))
LOCUS = CardSubType('Locus', (LAND,))
MINE = CardSubType('Mine', (LAND,))
MOUNTAIN = BasicLandType('Mountain', (LAND,))
PLAINS = BasicLandType('Plains', (LAND,))
POWER_PLANT = CardSubType('Power-Plant', (LAND,))
SWAMP = BasicLandType('Swamp', (LAND,))
TOWER = CardSubType('Tower', (LAND,))
URZAS = CardSubType('Urza’s', (LAND,))

AJANI = CardSubType('Ajani', (PLANESWALKER,))
ANGRATH = CardSubType('Angrath', (PLANESWALKER,))
ARLINN = CardSubType('Arlinn', (PLANESWALKER,))
ASHIOK = CardSubType('Ashiok', (PLANESWALKER,))
BOLAS = CardSubType('Bolas', (PLANESWALKER,))
CHANDRA = CardSubType('Chandra', (PLANESWALKER,))
DACK = CardSubType('Dack', (PLANESWALKER,))
DARETTI = CardSubType('Daretti', (PLANESWALKER,))
DOMRI = CardSubType('Domri', (PLANESWALKER,))
DOVIN = CardSubType('Dovin', (PLANESWALKER,))
ELSPETH = CardSubType('Elspeth', (PLANESWALKER,))
FREYALISE = CardSubType('Freyalise', (PLANESWALKER,))
GARRUK = CardSubType('Garruk', (PLANESWALKER,))
GIDEON = CardSubType('Gideon', (PLANESWALKER,))
HUATLI = CardSubType('Huatli', (PLANESWALKER,))
JACE = CardSubType('Jace', (PLANESWALKER,))
JAYA = CardSubType('Jaya', (PLANESWALKER,))
KARN = CardSubType('Karn', (PLANESWALKER,))
KAYA = CardSubType('Kaya', (PLANESWALKER,))
KIORA = CardSubType('Kiora', (PLANESWALKER,))
KOTH = CardSubType('Koth', (PLANESWALKER,))
LILIANA = CardSubType('Liliana', (PLANESWALKER,))
NAHIRI = CardSubType('Nahiri', (PLANESWALKER,))
NARSET = CardSubType('Narset', (PLANESWALKER,))
NISSA = CardSubType('Nissa', (PLANESWALKER,))
NIXILIS = CardSubType('Nixilis', (PLANESWALKER,))
RAL = CardSubType('Ral', (PLANESWALKER,))
SAHEELI = CardSubType('Saheeli', (PLANESWALKER,))
SAMUT = CardSubType('Samut', (PLANESWALKER,))
SARKHAN = CardSubType('Sarkhan', (PLANESWALKER,))
SORIN = CardSubType('Sorin', (PLANESWALKER,))
TAMIYO = CardSubType('Tamiyo', (PLANESWALKER,))
TEFERI = CardSubType('Teferi', (PLANESWALKER,))
TEZZERET = CardSubType('Tezzeret', (PLANESWALKER,))
TIBALT = CardSubType('Tibalt', (PLANESWALKER,))
UGIN = CardSubType('Ugin', (PLANESWALKER,))
VENSER = CardSubType('Venser', (PLANESWALKER,))
VRASKA = CardSubType('Vraska', (PLANESWALKER,))
XENAGOS = CardSubType('Xenagos', (PLANESWALKER,))
WILL = CardSubType('Will', (PLANESWALKER,))
ROWAN = CardSubType('Rowan', (PLANESWALKER,))
YANGGU = CardSubType('Yanggu', (PLANESWALKER,))
YANLING = CardSubType('Yanling', (PLANESWALKER,))

ARCANE = CardSubType('Arcane', (INSTANT, SORCERY))
TRAP = CardSubType('Trap', (INSTANT, SORCERY))

ADVISOR = CardSubType('Advisor', (CREATURE, TRIBAL))
AETHERBORN = CardSubType('Aetherborn', (CREATURE, TRIBAL))
ALLY = CardSubType('Ally', (CREATURE, TRIBAL))
ANGEL = CardSubType('Angel', (CREATURE, TRIBAL))
ANTELOPE = CardSubType('Antelope', (CREATURE, TRIBAL))
APE = CardSubType('Ape', (CREATURE, TRIBAL))
ARCHER = CardSubType('Archer', (CREATURE, TRIBAL))
ARCHON = CardSubType('Archon', (CREATURE, TRIBAL))
ARTIFICER = CardSubType('Artificer', (CREATURE, TRIBAL))
ASSASSIN = CardSubType('Assassin', (CREATURE, TRIBAL))
ASSEMBLY_WORKER = CardSubType('Assembly-Worker', (CREATURE, TRIBAL))
ATOG = CardSubType('Atog', (CREATURE, TRIBAL))
AUROCHS = CardSubType('Aurochs', (CREATURE, TRIBAL))
AVATAR = CardSubType('Avatar', (CREATURE, TRIBAL))
BADGER = CardSubType('Badger', (CREATURE, TRIBAL))
BARBARIAN = CardSubType('Barbarian', (CREATURE, TRIBAL))
BASILISK = CardSubType('Basilisk', (CREATURE, TRIBAL))
BAT = CardSubType('Bat', (CREATURE, TRIBAL))
BEAR = CardSubType('Bear', (CREATURE, TRIBAL))
BEAST = CardSubType('Beast', (CREATURE, TRIBAL))
BEEBLE = CardSubType('Beeble', (CREATURE, TRIBAL))
BERSERKER = CardSubType('Berserker', (CREATURE, TRIBAL))
BIRD = CardSubType('Bird', (CREATURE, TRIBAL))
BLINKMOTH = CardSubType('Blinkmoth', (CREATURE, TRIBAL))
BOAR = CardSubType('Boar', (CREATURE, TRIBAL))
BRINGER = CardSubType('Bringer', (CREATURE, TRIBAL))
BRUSHWAGG = CardSubType('Brushwagg', (CREATURE, TRIBAL))
CAMARID = CardSubType('Camarid', (CREATURE, TRIBAL))
CAMEL = CardSubType('Camel', (CREATURE, TRIBAL))
CARIBOU = CardSubType('Caribou', (CREATURE, TRIBAL))
CARRIER = CardSubType('Carrier', (CREATURE, TRIBAL))
CAT = CardSubType('Cat', (CREATURE, TRIBAL))
CENTAUR = CardSubType('Centaur', (CREATURE, TRIBAL))
CEPHALID = CardSubType('Cephalid', (CREATURE, TRIBAL))
CHIMERA = CardSubType('Chimera', (CREATURE, TRIBAL))
CITIZEN = CardSubType('Citizen', (CREATURE, TRIBAL))
CLERIC = CardSubType('Cleric', (CREATURE, TRIBAL))
COCKATRICE = CardSubType('Cockatrice', (CREATURE, TRIBAL))
CONSTRUCT = CardSubType('Construct', (CREATURE, TRIBAL))
COWARD = CardSubType('Coward', (CREATURE, TRIBAL))
CRAB = CardSubType('Crab', (CREATURE, TRIBAL))
CROCODILE = CardSubType('Crocodile', (CREATURE, TRIBAL))
CYCLOPS = CardSubType('Cyclops', (CREATURE, TRIBAL))
DAUTHI = CardSubType('Dauthi', (CREATURE, TRIBAL))
DEMON = CardSubType('Demon', (CREATURE, TRIBAL))
DESERTER = CardSubType('Deserter', (CREATURE, TRIBAL))
DEVIL = CardSubType('Devil', (CREATURE, TRIBAL))
DINOSAUR = CardSubType('Dinosaur', (CREATURE, TRIBAL))
DJINN = CardSubType('Djinn', (CREATURE, TRIBAL))
DRAGON = CardSubType('Dragon', (CREATURE, TRIBAL))
DRAKE = CardSubType('Drake', (CREATURE, TRIBAL))
DREADNOUGHT = CardSubType('Dreadnought', (CREATURE, TRIBAL))
DRONE = CardSubType('Drone', (CREATURE, TRIBAL))
DRUID = CardSubType('Druid', (CREATURE, TRIBAL))
DRYAD = CardSubType('Dryad', (CREATURE, TRIBAL))
DWARF = CardSubType('Dwarf', (CREATURE, TRIBAL))
EFREET = CardSubType('Efreet', (CREATURE, TRIBAL))
ELDER = CardSubType('Elder', (CREATURE, TRIBAL))
ELDRAZI = CardSubType('Eldrazi', (CREATURE, TRIBAL))
ELEMENTAL = CardSubType('Elemental', (CREATURE, TRIBAL))
ELEPHANT = CardSubType('Elephant', (CREATURE, TRIBAL))
ELF = CardSubType('Elf', (CREATURE, TRIBAL))
ELK = CardSubType('Elk', (CREATURE, TRIBAL))
EYE = CardSubType('Eye', (CREATURE, TRIBAL))
FAERIE = CardSubType('Faerie', (CREATURE, TRIBAL))
FERRET = CardSubType('Ferret', (CREATURE, TRIBAL))
FISH = CardSubType('Fish', (CREATURE, TRIBAL))
FLAGBEARER = CardSubType('Flagbearer', (CREATURE, TRIBAL))
FOX = CardSubType('Fox', (CREATURE, TRIBAL))
FROG = CardSubType('Frog', (CREATURE, TRIBAL))
FUNGUS = CardSubType('Fungus', (CREATURE, TRIBAL))
GARGOYLE = CardSubType('Gargoyle', (CREATURE, TRIBAL))
GERM = CardSubType('Germ', (CREATURE, TRIBAL))
GIANT = CardSubType('Giant', (CREATURE, TRIBAL))
GNOME = CardSubType('Gnome', (CREATURE, TRIBAL))
GOAT = CardSubType('Goat', (CREATURE, TRIBAL))
GOBLIN = CardSubType('Goblin', (CREATURE, TRIBAL))
GOD = CardSubType('God', (CREATURE, TRIBAL))
GOLEM = CardSubType('Golem', (CREATURE, TRIBAL))
GORGON = CardSubType('Gorgon', (CREATURE, TRIBAL))
GRAVEBORN = CardSubType('Graveborn', (CREATURE, TRIBAL))
GREMLIN = CardSubType('Gremlin', (CREATURE, TRIBAL))
GRIFFIN = CardSubType('Griffin', (CREATURE, TRIBAL))
HAG = CardSubType('Hag', (CREATURE, TRIBAL))
HARPY = CardSubType('Harpy', (CREATURE, TRIBAL))
HELLION = CardSubType('Hellion', (CREATURE, TRIBAL))
HIPPO = CardSubType('Hippo', (CREATURE, TRIBAL))
HIPPOGRIFF = CardSubType('Hippogriff', (CREATURE, TRIBAL))
HOMARID = CardSubType('Homarid', (CREATURE, TRIBAL))
HOMUNCULUS = CardSubType('Homunculus', (CREATURE, TRIBAL))
HORROR = CardSubType('Horror', (CREATURE, TRIBAL))
HORSE = CardSubType('Horse', (CREATURE, TRIBAL))
HOUND = CardSubType('Hound', (CREATURE, TRIBAL))
HUMAN = CardSubType('Human', (CREATURE, TRIBAL))
HYDRA = CardSubType('Hydra', (CREATURE, TRIBAL))
HYENA = CardSubType('Hyena', (CREATURE, TRIBAL))
ILLUSION = CardSubType('Illusion', (CREATURE, TRIBAL))
IMP = CardSubType('Imp', (CREATURE, TRIBAL))
INCARNATION = CardSubType('Incarnation', (CREATURE, TRIBAL))
INSECT = CardSubType('Insect', (CREATURE, TRIBAL))
JACKAL = CardSubType('Jackal', (CREATURE, TRIBAL))
JELLYFISH = CardSubType('Jellyfish', (CREATURE, TRIBAL))
JUGGERNAUT = CardSubType('Juggernaut', (CREATURE, TRIBAL))
KAVU = CardSubType('Kavu', (CREATURE, TRIBAL))
KIRIN = CardSubType('Kirin', (CREATURE, TRIBAL))
KITHKIN = CardSubType('Kithkin', (CREATURE, TRIBAL))
KNIGHT = CardSubType('Knight', (CREATURE, TRIBAL))
KOBOLD = CardSubType('Kobold', (CREATURE, TRIBAL))
KOR = CardSubType('Kor', (CREATURE, TRIBAL))
KRAKEN = CardSubType('Kraken', (CREATURE, TRIBAL))
LAMIA = CardSubType('Lamia', (CREATURE, TRIBAL))
LAMMASU = CardSubType('Lammasu', (CREATURE, TRIBAL))
LEECH = CardSubType('Leech', (CREATURE, TRIBAL))
LEVIATHAN = CardSubType('Leviathan', (CREATURE, TRIBAL))
LHURGOYF = CardSubType('Lhurgoyf', (CREATURE, TRIBAL))
LICID = CardSubType('Licid', (CREATURE, TRIBAL))
LIZARD = CardSubType('Lizard', (CREATURE, TRIBAL))
MANTICORE = CardSubType('Manticore', (CREATURE, TRIBAL))
MASTICORE = CardSubType('Masticore', (CREATURE, TRIBAL))
MERCENARY = CardSubType('Mercenary', (CREATURE, TRIBAL))
MERFOLK = CardSubType('Merfolk', (CREATURE, TRIBAL))
METATHRAN = CardSubType('Metathran', (CREATURE, TRIBAL))
MINION = CardSubType('Minion', (CREATURE, TRIBAL))
MINOTAUR = CardSubType('Minotaur', (CREATURE, TRIBAL))
MOLE = CardSubType('Mole', (CREATURE, TRIBAL))
MONGER = CardSubType('Monger', (CREATURE, TRIBAL))
MONGOOSE = CardSubType('Mongoose', (CREATURE, TRIBAL))
MONK = CardSubType('Monk', (CREATURE, TRIBAL))
MONKEY = CardSubType('Monkey', (CREATURE, TRIBAL))
MOONFOLK = CardSubType('Moonfolk', (CREATURE, TRIBAL))
MUTANT = CardSubType('Mutant', (CREATURE, TRIBAL))
MYR = CardSubType('Myr', (CREATURE, TRIBAL))
MYSTIC = CardSubType('Mystic', (CREATURE, TRIBAL))
NAGA = CardSubType('Naga', (CREATURE, TRIBAL))
NAUTILUS = CardSubType('Nautilus', (CREATURE, TRIBAL))
NEPHILIM = CardSubType('Nephilim', (CREATURE, TRIBAL))
NIGHTMARE = CardSubType('Nightmare', (CREATURE, TRIBAL))
NIGHTSTALKER = CardSubType('Nightstalker', (CREATURE, TRIBAL))
NINJA = CardSubType('Ninja', (CREATURE, TRIBAL))
NOGGLE = CardSubType('Noggle', (CREATURE, TRIBAL))
NOMAD = CardSubType('Nomad', (CREATURE, TRIBAL))
NYMPH = CardSubType('Nymph', (CREATURE, TRIBAL))
OCTOPUS = CardSubType('Octopus', (CREATURE, TRIBAL))
OGRE = CardSubType('Ogre', (CREATURE, TRIBAL))
OOZE = CardSubType('Ooze', (CREATURE, TRIBAL))
ORB = CardSubType('Orb', (CREATURE, TRIBAL))
ORC = CardSubType('Orc', (CREATURE, TRIBAL))
ORGG = CardSubType('Orgg', (CREATURE, TRIBAL))
OUPHE = CardSubType('Ouphe', (CREATURE, TRIBAL))
OX = CardSubType('Ox', (CREATURE, TRIBAL))
OYSTER = CardSubType('Oyster', (CREATURE, TRIBAL))
PEGASUS = CardSubType('Pegasus', (CREATURE, TRIBAL))
PENTAVITE = CardSubType('Pentavite', (CREATURE, TRIBAL))
PEST = CardSubType('Pest', (CREATURE, TRIBAL))
PHELDDAGRIF = CardSubType('Phelddagrif', (CREATURE, TRIBAL))
PHOENIX = CardSubType('Phoenix', (CREATURE, TRIBAL))
PILOT = CardSubType('Pilot', (CREATURE, TRIBAL))
PINCHER = CardSubType('Pincher', (CREATURE, TRIBAL))
PIRATE = CardSubType('Pirate', (CREATURE, TRIBAL))
PLANT = CardSubType('Plant', (CREATURE, TRIBAL))
PRAETOR = CardSubType('Praetor', (CREATURE, TRIBAL))
PRISM = CardSubType('Prism', (CREATURE, TRIBAL))
PROCESSOR = CardSubType('Processor', (CREATURE, TRIBAL))
RABBIT = CardSubType('Rabbit', (CREATURE, TRIBAL))
RAT = CardSubType('Rat', (CREATURE, TRIBAL))
REBEL = CardSubType('Rebel', (CREATURE, TRIBAL))
REFLECTION = CardSubType('Reflection', (CREATURE, TRIBAL))
RHINO = CardSubType('Rhino', (CREATURE, TRIBAL))
RIGGER = CardSubType('Rigger', (CREATURE, TRIBAL))
ROGUE = CardSubType('Rogue', (CREATURE, TRIBAL))
SABLE = CardSubType('Sable', (CREATURE, TRIBAL))
SALAMANDER = CardSubType('Salamander', (CREATURE, TRIBAL))
SAMURAI = CardSubType('Samurai', (CREATURE, TRIBAL))
SAND = CardSubType('Sand', (CREATURE, TRIBAL))
SAPROLING = CardSubType('Saproling', (CREATURE, TRIBAL))
SATYR = CardSubType('Satyr', (CREATURE, TRIBAL))
SCARECROW = CardSubType('Scarecrow', (CREATURE, TRIBAL))
SCION = CardSubType('Scion', (CREATURE, TRIBAL))
SCORPION = CardSubType('Scorpion', (CREATURE, TRIBAL))
SCOUT = CardSubType('Scout', (CREATURE, TRIBAL))
SERF = CardSubType('Serf', (CREATURE, TRIBAL))
SERPENT = CardSubType('Serpent', (CREATURE, TRIBAL))
SERVO = CardSubType('Servo', (CREATURE, TRIBAL))
SHADE = CardSubType('Shade', (CREATURE, TRIBAL))
SHAMAN = CardSubType('Shaman', (CREATURE, TRIBAL))
SHAPESHIFTER = CardSubType('Shapeshifter', (CREATURE, TRIBAL))
SHEEP = CardSubType('Sheep', (CREATURE, TRIBAL))
SIREN = CardSubType('Siren', (CREATURE, TRIBAL))
SKELETON = CardSubType('Skeleton', (CREATURE, TRIBAL))
SLITH = CardSubType('Slith', (CREATURE, TRIBAL))
SLIVER = CardSubType('Sliver', (CREATURE, TRIBAL))
SLUG = CardSubType('Slug', (CREATURE, TRIBAL))
SNAKE = CardSubType('Snake', (CREATURE, TRIBAL))
SOLDIER = CardSubType('Soldier', (CREATURE, TRIBAL))
SOLTARI = CardSubType('Soltari', (CREATURE, TRIBAL))
SPAWN = CardSubType('Spawn', (CREATURE, TRIBAL))
SPECTER = CardSubType('Specter', (CREATURE, TRIBAL))
SPELLSHAPER = CardSubType('Spellshaper', (CREATURE, TRIBAL))
SPHINX = CardSubType('Sphinx', (CREATURE, TRIBAL))
SPIDER = CardSubType('Spider', (CREATURE, TRIBAL))
SPIKE = CardSubType('Spike', (CREATURE, TRIBAL))
SPIRIT = CardSubType('Spirit', (CREATURE, TRIBAL))
SPLINTER = CardSubType('Splinter', (CREATURE, TRIBAL))
SPONGE = CardSubType('Sponge', (CREATURE, TRIBAL))
SQUID = CardSubType('Squid', (CREATURE, TRIBAL))
SQUIRREL = CardSubType('Squirrel', (CREATURE, TRIBAL))
STARFISH = CardSubType('Starfish', (CREATURE, TRIBAL))
SURRAKAR = CardSubType('Surrakar', (CREATURE, TRIBAL))
SURVIVOR = CardSubType('Survivor', (CREATURE, TRIBAL))
TETRAVITE = CardSubType('Tetravite', (CREATURE, TRIBAL))
THALAKOS = CardSubType('Thalakos', (CREATURE, TRIBAL))
THOPTER = CardSubType('Thopter', (CREATURE, TRIBAL))
THRULL = CardSubType('Thrull', (CREATURE, TRIBAL))
TREEFOLK = CardSubType('Treefolk', (CREATURE, TRIBAL))
TRILOBITE = CardSubType('Trilobite', (CREATURE, TRIBAL))
TRISKELAVITE = CardSubType('Triskelavite', (CREATURE, TRIBAL))
TROLL = CardSubType('Troll', (CREATURE, TRIBAL))
TURTLE = CardSubType('Turtle', (CREATURE, TRIBAL))
UNICORN = CardSubType('Unicorn', (CREATURE, TRIBAL))
VAMPIRE = CardSubType('Vampire', (CREATURE, TRIBAL))
VEDALKEN = CardSubType('Vedalken', (CREATURE, TRIBAL))
VIASHINO = CardSubType('Viashino', (CREATURE, TRIBAL))
VOLVER = CardSubType('Volver', (CREATURE, TRIBAL))
WALL = CardSubType('Wall', (CREATURE, TRIBAL))
WARRIOR = CardSubType('Warrior', (CREATURE, TRIBAL))
WEIRD = CardSubType('Weird', (CREATURE, TRIBAL))
WEREWOLF = CardSubType('Werewolf', (CREATURE, TRIBAL))
WHALE = CardSubType('Whale', (CREATURE, TRIBAL))
WIZARD = CardSubType('Wizard', (CREATURE, TRIBAL))
WOLF = CardSubType('Wolf', (CREATURE, TRIBAL))
WOLVERINE = CardSubType('Wolverine', (CREATURE, TRIBAL))
WOMBAT = CardSubType('Wombat', (CREATURE, TRIBAL))
WORM = CardSubType('Worm', (CREATURE, TRIBAL))
WRAITH = CardSubType('Wraith', (CREATURE, TRIBAL))
WURM = CardSubType('Wurm', (CREATURE, TRIBAL))
YETI = CardSubType('Yeti', (CREATURE, TRIBAL))
ZOMBIE = CardSubType('Zombie', (CREATURE, TRIBAL))
ZUBERA = CardSubType('Zubera', (CREATURE, TRIBAL))
AZRA = CardSubType('Azra', (CREATURE, TRIBAL))

BASIC_LAND_TYPES = (
	PLAINS,
	ISLAND,
	SWAMP,
	MOUNTAIN,
	FOREST,
)

ALL_TYPES = tuple(
	member
	for name, member in
	inspect.getmembers(sys.modules[__name__])
	if isinstance(member, BaseCardType)
)


class TypeLine(object):
	SEPARATOR = ' — '

	def __init__(self, *types: BaseCardType):
		self._types = frozenset(types)
		self._repr = None #type: t.Optional[str]

	def __eq__(self, other):
		return (
			isinstance(other, TypeLine)
			and self._types == other.types
		)

	def __gt__(self, other):
		return (
			isinstance(other, TypeLine)
			and self._types > other.types
		)

	def __ge__(self, other):
		return (
			isinstance(other, TypeLine)
			and self._types >= other.types
		)

	def __lt__(self, other):
		return (
			isinstance(other, TypeLine)
			and self._types < other.types
		)

	def __le__(self, other):
		return (
			isinstance(other, TypeLine)
			and self._types <= other.types
		)

	def __hash__(self):
		return hash(self._types)

	def __repr__(self):
		if self._repr is not None:
			return  self._repr

		self._repr = ' '.join(
			str(card_type)
			for card_type in
			itertools.chain(
				sorted(self.super_types),
				sorted(self.card_types),
			)
		)

		if self.sub_types:
			self._repr += TypeLine.SEPARATOR + ' '.join(
				str(sub_type)
				for sub_type in
				sorted(self.sub_types)
			)

		return self._repr

	def __iter__(self):
		return self._types.__iter__()

	def __contains__(self, item):
		if isinstance(item, self.__class__):
			return item._types.issubset(self._types)
		return item in self._types

	@property
	def types(self) -> t.AbstractSet[BaseCardType]:
		return self._types

	@LazyProperty
	def super_types(self) -> t.Set[CardSuperType]:
		return {t for t in self._types if isinstance(t, CardSuperType)}

	@LazyProperty
	def card_types(self) -> t.Set[CardType]:
		return {t for t in self._types if isinstance(t, CardType)}

	@LazyProperty
	def sub_types(self) -> t.Set[CardSubType]:
		return {t for t in self._types if isinstance(t, CardSubType)}



def test():
	import pickle

	s = pickle.dumps(CREATURE)

	angel = pickle.loads(s) #type: CardType

	print(angel, angel.sub_types)


if __name__ == '__main__':
	test()