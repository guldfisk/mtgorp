import inspect
import itertools
import sys
import typing as t
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
    def __init__(self, name: str, is_permanent: bool = False):
        super().__init__(name)
        self.sub_types: t.AbstractSet[CardSubType] = frozenset()
        self._is_permanent = is_permanent

    @property
    def is_permanent(self) -> bool:
        return self._is_permanent

    def __lt__(self, other):
        return _CARD_TYPE_INDEX.get(self, -1) < _CARD_TYPE_INDEX.get(other, -1)

    def __reduce__(self):
        return (
            self.__class__,
            (self._name,),
            {"sub_types": self.sub_types},
        )


class CardSubType(BaseCardType):
    def __init__(self, name: str, card_types: t.Optional[t.Iterable[CardType]] = None):
        super().__init__(name)

        if card_types is None:
            self.card_types = frozenset()
            return

        self.card_types: t.AbstractSet[CardType] = frozenset(card_types)

        for card_type in card_types:
            card_type.sub_types |= frozenset((self,))

    def __reduce__(self):
        return (
            self.__class__,
            (self._name,),
            {"card_types": self.card_types},
        )


class BasicLandType(CardSubType):
    pass


SNOW = CardSuperType("Snow")
LEGENDARY = CardSuperType("Legendary")
WORLD = CardSuperType("World")
BASIC = CardSuperType("Basic")

SUPER_TYPES = (
    LEGENDARY,
    BASIC,
    WORLD,
    SNOW,
)

CREATURE = CardType("Creature", is_permanent=True)
ARTIFACT = CardType("Artifact", is_permanent=True)
ENCHANTMENT = CardType("Enchantment", is_permanent=True)
LAND = CardType("Land", is_permanent=True)
PLANESWALKER = CardType("Planeswalker", is_permanent=True)
INSTANT = CardType("Instant")
SORCERY = CardType("Sorcery")
TRIBAL = CardType("Tribal")

CARD_TYPES = (TRIBAL, ENCHANTMENT, ARTIFACT, LAND, CREATURE, PLANESWALKER, INSTANT, SORCERY)

_SUPER_TYPE_INDEX = {t: idx for idx, t in enumerate(SUPER_TYPES)}

_CARD_TYPE_INDEX = {t: idx for idx, t in enumerate(CARD_TYPES)}

ATTRACTION = CardSubType("Attraction", (ARTIFACT,))
BLOOD = CardSubType("Blood", (ARTIFACT,))
CLUE = CardSubType("Clue", (ARTIFACT,))
CONTRAPTION = CardSubType("Contraption", (ARTIFACT,))
EQUIPMENT = CardSubType("Equipment", (ARTIFACT,))
FOOD = CardSubType("Food", (ARTIFACT,))
FORTIFICATION = CardSubType("Fortification", (ARTIFACT,))
GOLD = CardSubType("Gold", (ARTIFACT,))
INCUBATOR = CardSubType("Incubator", (ARTIFACT,))
POWERSTONE = CardSubType("Powerstone", (ARTIFACT,))
TREASURE = CardSubType("Treasure", (ARTIFACT,))
VEHICLE = CardSubType("Vehicle", (ARTIFACT,))

AURA = CardSubType("Aura", (ENCHANTMENT,))
BACKGROUND = CardSubType("Background", (ENCHANTMENT,))
CARTOUCHE = CardSubType("Cartouche", (ENCHANTMENT,))
CLASS = CardSubType("Class", (ENCHANTMENT,))
CURSE = CardSubType("Curse", (ENCHANTMENT,))
RUNE = CardSubType("Rune", (ENCHANTMENT,))
ROLE = CardSubType("Role", (ENCHANTMENT,))
SAGA = CardSubType("Saga", (ENCHANTMENT,))
SHARD = CardSubType("Shard", (ENCHANTMENT,))
SHRINE = CardSubType("Shrine", (ENCHANTMENT,))

CAVE = CardSubType("Cave", (LAND,))
DESERT = CardSubType("Desert", (LAND,))
FOREST = BasicLandType("Forest", (LAND,))
GATE = CardSubType("Gate", (LAND,))
ISLAND = BasicLandType("Island", (LAND,))
LAIR = CardSubType("Lair", (LAND,))
LOCUS = CardSubType("Locus", (LAND,))
MINE = CardSubType("Mine", (LAND,))
MOUNTAIN = BasicLandType("Mountain", (LAND,))
PLAINS = BasicLandType("Plains", (LAND,))
POWER_PLANT = CardSubType("Power-Plant", (LAND,))
SWAMP = BasicLandType("Swamp", (LAND,))
TOWER = CardSubType("Tower", (LAND,))
URZAS = CardSubType("Urza’s", (LAND,))

AJANI = CardSubType("Ajani", (PLANESWALKER,))
AMINATOU = CardSubType("Aminatou", (PLANESWALKER,))
ANGRATH = CardSubType("Angrath", (PLANESWALKER,))
ARLINN = CardSubType("Arlinn", (PLANESWALKER,))
ASHIOK = CardSubType("Ashiok", (PLANESWALKER,))
BAHAMUT = CardSubType("Bahamut", (PLANESWALKER,))
BASRI = CardSubType("Basri", (PLANESWALKER,))
BOLAS = CardSubType("Bolas", (PLANESWALKER,))
CALIX = CardSubType("Calix", (PLANESWALKER,))
CHANDRA = CardSubType("Chandra", (PLANESWALKER,))
COMET = CardSubType("Comet", (PLANESWALKER,))
DACK = CardSubType("Dack", (PLANESWALKER,))
DAKKON = CardSubType("Dakkon", (PLANESWALKER,))
DARETTI = CardSubType("Daretti", (PLANESWALKER,))
DAVRIEL = CardSubType("Davriel", (PLANESWALKER,))
DIHADA = CardSubType("Dihada", (PLANESWALKER,))
DOMRI = CardSubType("Domri", (PLANESWALKER,))
DOVIN = CardSubType("Dovin", (PLANESWALKER,))
ELLYWICK = CardSubType("Ellywick", (PLANESWALKER,))
ELMINSTER = CardSubType("Elminster", (PLANESWALKER,))
ELSPETH = CardSubType("Elspeth", (PLANESWALKER,))
ESTRID = CardSubType("Estrid", (PLANESWALKER,))
FREYALISE = CardSubType("Freyalise", (PLANESWALKER,))
GARRUK = CardSubType("Garruk", (PLANESWALKER,))
GIDEON = CardSubType("Gideon", (PLANESWALKER,))
GRIST = CardSubType("Grist", (PLANESWALKER,))
GUFF = CardSubType("Guff", (PLANESWALKER,))
HUATLI = CardSubType("Huatli", (PLANESWALKER,))
JACE = CardSubType("Jace", (PLANESWALKER,))
JARED = CardSubType("Jared", (PLANESWALKER,))
JAYA = CardSubType("Jaya", (PLANESWALKER,))
JESKA = CardSubType("Jeska", (PLANESWALKER,))
KAITO = CardSubType("Kaito", (PLANESWALKER,))
KARN = CardSubType("Karn", (PLANESWALKER,))
KASMINA = CardSubType("Kasmina", (PLANESWALKER,))
KAYA = CardSubType("Kaya", (PLANESWALKER,))
KIORA = CardSubType("Kiora", (PLANESWALKER,))
KOTH = CardSubType("Koth", (PLANESWALKER,))
LILIANA = CardSubType("Liliana", (PLANESWALKER,))
LOLTH = CardSubType("Lolth", (PLANESWALKER,))
LUKKA = CardSubType("Lukka", (PLANESWALKER,))
MINSC = CardSubType("Minsc", (PLANESWALKER,))
MORDENKAINEN = CardSubType("Mordenkainen", (PLANESWALKER,))
NAHIRI = CardSubType("Nahiri", (PLANESWALKER,))
NARSET = CardSubType("Narset", (PLANESWALKER,))
NIKO = CardSubType("Niko", (PLANESWALKER,))
NISSA = CardSubType("Nissa", (PLANESWALKER,))
NIXILIS = CardSubType("Nixilis", (PLANESWALKER,))
OKO = CardSubType("Oko", (PLANESWALKER,))
RAL = CardSubType("Ral", (PLANESWALKER,))
ROWAN = CardSubType("Rowan", (PLANESWALKER,))
SAHEELI = CardSubType("Saheeli", (PLANESWALKER,))
SAMUT = CardSubType("Samut", (PLANESWALKER,))
SARKHAN = CardSubType("Sarkhan", (PLANESWALKER,))
SERRA = CardSubType("Serra", (PLANESWALKER,))
SIVITRI = CardSubType("Sivitri", (PLANESWALKER,))
SORIN = CardSubType("Sorin", (PLANESWALKER,))
SZAT = CardSubType("Szat", (PLANESWALKER,))
TAMIYO = CardSubType("Tamiyo", (PLANESWALKER,))
TASHA = CardSubType("Tasha", (PLANESWALKER,))
TEFERI = CardSubType("Teferi", (PLANESWALKER,))
TEYO = CardSubType("Teyo", (PLANESWALKER,))
TEZZERET = CardSubType("Tezzeret", (PLANESWALKER,))
TIBALT = CardSubType("Tibalt", (PLANESWALKER,))
TYVAR = CardSubType("Tyvar", (PLANESWALKER,))
UGIN = CardSubType("Ugin", (PLANESWALKER,))
URZA = CardSubType("Urza", (PLANESWALKER,))
VENSER = CardSubType("Venser", (PLANESWALKER,))
VIVIEN = CardSubType("Vivien", (PLANESWALKER,))
VRASKA = CardSubType("Vraska", (PLANESWALKER,))
VRONOS = CardSubType("Vronos", (PLANESWALKER,))
WILL = CardSubType("Will", (PLANESWALKER,))
WINDGRACE = CardSubType("Windgrace", (PLANESWALKER,))
WRENN = CardSubType("Wrenn", (PLANESWALKER,))
XENAGOS = CardSubType("Xenagos", (PLANESWALKER,))
YANGGU = CardSubType("Yanggu", (PLANESWALKER,))
YANLING = CardSubType("Yanling", (PLANESWALKER,))
ZARIEL = CardSubType("Zariel", (PLANESWALKER,))

ADVENTURE = CardSubType("Adventure", (INSTANT, SORCERY))
ARCANE = CardSubType("Arcane", (INSTANT, SORCERY))
LESSON = CardSubType("Lesson", (INSTANT, SORCERY))
TRAP = CardSubType("Trap", (INSTANT, SORCERY))

ADVISOR = CardSubType("Advisor", (CREATURE, TRIBAL))
AETHERBORN = CardSubType("Aetherborn", (CREATURE, TRIBAL))
ALIEN = CardSubType("Alien", (CREATURE, TRIBAL))
ALLY = CardSubType("Ally", (CREATURE, TRIBAL))
ANGEL = CardSubType("Angel", (CREATURE, TRIBAL))
ANTELOPE = CardSubType("Antelope", (CREATURE, TRIBAL))
APE = CardSubType("Ape", (CREATURE, TRIBAL))
ARCHER = CardSubType("Archer", (CREATURE, TRIBAL))
ARCHON = CardSubType("Archon", (CREATURE, TRIBAL))
ARMY = CardSubType("Army", (CREATURE, TRIBAL))
ARTIFICER = CardSubType("Artificer", (CREATURE, TRIBAL))
ASSASSIN = CardSubType("Assassin", (CREATURE, TRIBAL))
ASSEMBLY_WORKER = CardSubType("Assembly-Worker", (CREATURE, TRIBAL))
ASTARTES = CardSubType("Astartes", (CREATURE, TRIBAL))
ATOG = CardSubType("Atog", (CREATURE, TRIBAL))
AUROCHS = CardSubType("Aurochs", (CREATURE, TRIBAL))
AVATAR = CardSubType("Avatar", (CREATURE, TRIBAL))
AZRA = CardSubType("Azra", (CREATURE, TRIBAL))
BADGER = CardSubType("Badger", (CREATURE, TRIBAL))
BALLOON = CardSubType("Balloon", (CREATURE, TRIBAL))
BARBARIAN = CardSubType("Barbarian", (CREATURE, TRIBAL))
BARD = CardSubType("Bard", (CREATURE, TRIBAL))
BASILISK = CardSubType("Basilisk", (CREATURE, TRIBAL))
BAT = CardSubType("Bat", (CREATURE, TRIBAL))
BEAR = CardSubType("Bear", (CREATURE, TRIBAL))
BEAST = CardSubType("Beast", (CREATURE, TRIBAL))
BEEBLE = CardSubType("Beeble", (CREATURE, TRIBAL))
BEHOLDER = CardSubType("Beholder", (CREATURE, TRIBAL))
BERSERKER = CardSubType("Berserker", (CREATURE, TRIBAL))
BIRD = CardSubType("Bird", (CREATURE, TRIBAL))
BLINKMOTH = CardSubType("Blinkmoth", (CREATURE, TRIBAL))
BOAR = CardSubType("Boar", (CREATURE, TRIBAL))
BRINGER = CardSubType("Bringer", (CREATURE, TRIBAL))
BRUSHWAGG = CardSubType("Brushwagg", (CREATURE, TRIBAL))
CAMARID = CardSubType("Camarid", (CREATURE, TRIBAL))
CAMEL = CardSubType("Camel", (CREATURE, TRIBAL))
CAPYBARA = CardSubType("Capybara", (CREATURE, TRIBAL))
CARIBOU = CardSubType("Caribou", (CREATURE, TRIBAL))
CARRIER = CardSubType("Carrier", (CREATURE, TRIBAL))
CAT = CardSubType("Cat", (CREATURE, TRIBAL))
CENTAUR = CardSubType("Centaur", (CREATURE, TRIBAL))
CEPHALID = CardSubType("Cephalid", (CREATURE, TRIBAL))
CHILD = CardSubType("Child", (CREATURE, TRIBAL))
CHIMERA = CardSubType("Chimera", (CREATURE, TRIBAL))
CITIZEN = CardSubType("Citizen", (CREATURE, TRIBAL))
CLERIC = CardSubType("Cleric", (CREATURE, TRIBAL))
CLOWN = CardSubType("Clown", (CREATURE, TRIBAL))
COCKATRICE = CardSubType("Cockatrice", (CREATURE, TRIBAL))
CONSTRUCT = CardSubType("Construct", (CREATURE, TRIBAL))
COWARD = CardSubType("Coward", (CREATURE, TRIBAL))
CRAB = CardSubType("Crab", (CREATURE, TRIBAL))
CROCODILE = CardSubType("Crocodile", (CREATURE, TRIBAL))
C_TAN = CardSubType("C’tan", (CREATURE, TRIBAL))
CUSTODES = CardSubType("Custodes", (CREATURE, TRIBAL))
CYBERMAN = CardSubType("Cyberman", (CREATURE, TRIBAL))
CYCLOPS = CardSubType("Cyclops", (CREATURE, TRIBAL))
DALEK = CardSubType("Dalek", (CREATURE, TRIBAL))
DAUTHI = CardSubType("Dauthi", (CREATURE, TRIBAL))
DEMIGOD = CardSubType("Demigod", (CREATURE, TRIBAL))
DEMON = CardSubType("Demon", (CREATURE, TRIBAL))
DESERTER = CardSubType("Deserter", (CREATURE, TRIBAL))
DETECTIVE = CardSubType("Detective", (CREATURE, TRIBAL))
DEVIL = CardSubType("Devil", (CREATURE, TRIBAL))
DINOSAUR = CardSubType("Dinosaur", (CREATURE, TRIBAL))
DJINN = CardSubType("Djinn", (CREATURE, TRIBAL))
DOCTOR = CardSubType("Doctor", (CREATURE, TRIBAL))
DOG = CardSubType("Dog", (CREATURE, TRIBAL))
DRAGON = CardSubType("Dragon", (CREATURE, TRIBAL))
DRAKE = CardSubType("Drake", (CREATURE, TRIBAL))
DREADNOUGHT = CardSubType("Dreadnought", (CREATURE, TRIBAL))
DRONE = CardSubType("Drone", (CREATURE, TRIBAL))
DRUID = CardSubType("Druid", (CREATURE, TRIBAL))
DRYAD = CardSubType("Dryad", (CREATURE, TRIBAL))
DWARF = CardSubType("Dwarf", (CREATURE, TRIBAL))
EFREET = CardSubType("Efreet", (CREATURE, TRIBAL))
EGG = CardSubType("Egg", (CREATURE, TRIBAL))
ELDER = CardSubType("Elder", (CREATURE, TRIBAL))
ELDRAZI = CardSubType("Eldrazi", (CREATURE, TRIBAL))
ELEMENTAL = CardSubType("Elemental", (CREATURE, TRIBAL))
ELEPHANT = CardSubType("Elephant", (CREATURE, TRIBAL))
ELF = CardSubType("Elf", (CREATURE, TRIBAL))
ELK = CardSubType("Elk", (CREATURE, TRIBAL))
EMPLOYEE = CardSubType("Employee", (CREATURE, TRIBAL))
EYE = CardSubType("Eye", (CREATURE, TRIBAL))
FAERIE = CardSubType("Faerie", (CREATURE, TRIBAL))
FERRET = CardSubType("Ferret", (CREATURE, TRIBAL))
FISH = CardSubType("Fish", (CREATURE, TRIBAL))
FLAGBEARER = CardSubType("Flagbearer", (CREATURE, TRIBAL))
FOX = CardSubType("Fox", (CREATURE, TRIBAL))
FRACTAL = CardSubType("Fractal", (CREATURE, TRIBAL))
FROG = CardSubType("Frog", (CREATURE, TRIBAL))
FUNGUS = CardSubType("Fungus", (CREATURE, TRIBAL))
GAMER = CardSubType("Gamer", (CREATURE, TRIBAL))
GARGOYLE = CardSubType("Gargoyle", (CREATURE, TRIBAL))
GERM = CardSubType("Germ", (CREATURE, TRIBAL))
GIANT = CardSubType("Giant", (CREATURE, TRIBAL))
GITH = CardSubType("Gith", (CREATURE, TRIBAL))
GNOLL = CardSubType("Gnoll", (CREATURE, TRIBAL))
GNOME = CardSubType("Gnome", (CREATURE, TRIBAL))
GOAT = CardSubType("Goat", (CREATURE, TRIBAL))
GOBLIN = CardSubType("Goblin", (CREATURE, TRIBAL))
GOD = CardSubType("God", (CREATURE, TRIBAL))
GOLEM = CardSubType("Golem", (CREATURE, TRIBAL))
GORGON = CardSubType("Gorgon", (CREATURE, TRIBAL))
GRAVEBORN = CardSubType("Graveborn", (CREATURE, TRIBAL))
GREMLIN = CardSubType("Gremlin", (CREATURE, TRIBAL))
GRIFFIN = CardSubType("Griffin", (CREATURE, TRIBAL))
GUEST = CardSubType("Guest", (CREATURE, TRIBAL))
HAG = CardSubType("Hag", (CREATURE, TRIBAL))
HALFLING = CardSubType("Halfling", (CREATURE, TRIBAL))
HAMSTER = CardSubType("Hamster", (CREATURE, TRIBAL))
HARPY = CardSubType("Harpy", (CREATURE, TRIBAL))
HELLION = CardSubType("Hellion", (CREATURE, TRIBAL))
HIPPO = CardSubType("Hippo", (CREATURE, TRIBAL))
HIPPOGRIFF = CardSubType("Hippogriff", (CREATURE, TRIBAL))
HOMARID = CardSubType("Homarid", (CREATURE, TRIBAL))
HOMUNCULUS = CardSubType("Homunculus", (CREATURE, TRIBAL))
HORROR = CardSubType("Horror", (CREATURE, TRIBAL))
HORSE = CardSubType("Horse", (CREATURE, TRIBAL))
HUMAN = CardSubType("Human", (CREATURE, TRIBAL))
HYDRA = CardSubType("Hydra", (CREATURE, TRIBAL))
HYENA = CardSubType("Hyena", (CREATURE, TRIBAL))
ILLUSION = CardSubType("Illusion", (CREATURE, TRIBAL))
IMP = CardSubType("Imp", (CREATURE, TRIBAL))
INCARNATION = CardSubType("Incarnation", (CREATURE, TRIBAL))
INKLING = CardSubType("Inkling", (CREATURE, TRIBAL))
INQUISITOR = CardSubType("Inquisitor", (CREATURE, TRIBAL))
INSECT = CardSubType("Insect", (CREATURE, TRIBAL))
JACKAL = CardSubType("Jackal", (CREATURE, TRIBAL))
JELLYFISH = CardSubType("Jellyfish", (CREATURE, TRIBAL))
JUGGERNAUT = CardSubType("Juggernaut", (CREATURE, TRIBAL))
KAVU = CardSubType("Kavu", (CREATURE, TRIBAL))
KIRIN = CardSubType("Kirin", (CREATURE, TRIBAL))
KITHKIN = CardSubType("Kithkin", (CREATURE, TRIBAL))
KNIGHT = CardSubType("Knight", (CREATURE, TRIBAL))
KOBOLD = CardSubType("Kobold", (CREATURE, TRIBAL))
KOR = CardSubType("Kor", (CREATURE, TRIBAL))
KRAKEN = CardSubType("Kraken", (CREATURE, TRIBAL))
LAMIA = CardSubType("Lamia", (CREATURE, TRIBAL))
LAMMASU = CardSubType("Lammasu", (CREATURE, TRIBAL))
LEECH = CardSubType("Leech", (CREATURE, TRIBAL))
LEVIATHAN = CardSubType("Leviathan", (CREATURE, TRIBAL))
LHURGOYF = CardSubType("Lhurgoyf", (CREATURE, TRIBAL))
LICID = CardSubType("Licid", (CREATURE, TRIBAL))
LIZARD = CardSubType("Lizard", (CREATURE, TRIBAL))
MANTICORE = CardSubType("Manticore", (CREATURE, TRIBAL))
MASTICORE = CardSubType("Masticore", (CREATURE, TRIBAL))
MERCENARY = CardSubType("Mercenary", (CREATURE, TRIBAL))
MERFOLK = CardSubType("Merfolk", (CREATURE, TRIBAL))
METATHRAN = CardSubType("Metathran", (CREATURE, TRIBAL))
MINION = CardSubType("Minion", (CREATURE, TRIBAL))
MINOTAUR = CardSubType("Minotaur", (CREATURE, TRIBAL))
MITE = CardSubType("Mite", (CREATURE, TRIBAL))
MOLE = CardSubType("Mole", (CREATURE, TRIBAL))
MONGER = CardSubType("Monger", (CREATURE, TRIBAL))
MONGOOSE = CardSubType("Mongoose", (CREATURE, TRIBAL))
MONK = CardSubType("Monk", (CREATURE, TRIBAL))
MONKEY = CardSubType("Monkey", (CREATURE, TRIBAL))
MOONFOLK = CardSubType("Moonfolk", (CREATURE, TRIBAL))
MOUSE = CardSubType("Mouse", (CREATURE, TRIBAL))
MUTANT = CardSubType("Mutant", (CREATURE, TRIBAL))
MYR = CardSubType("Myr", (CREATURE, TRIBAL))
MYSTIC = CardSubType("Mystic", (CREATURE, TRIBAL))
NAGA = CardSubType("Naga", (CREATURE, TRIBAL))
NAUTILUS = CardSubType("Nautilus", (CREATURE, TRIBAL))
NECRON = CardSubType("Necron", (CREATURE, TRIBAL))
NEPHILIM = CardSubType("Nephilim", (CREATURE, TRIBAL))
NIGHTMARE = CardSubType("Nightmare", (CREATURE, TRIBAL))
NIGHTSTALKER = CardSubType("Nightstalker", (CREATURE, TRIBAL))
NINJA = CardSubType("Ninja", (CREATURE, TRIBAL))
NOBLE = CardSubType("Noble", (CREATURE, TRIBAL))
NOGGLE = CardSubType("Noggle", (CREATURE, TRIBAL))
NOMAD = CardSubType("Nomad", (CREATURE, TRIBAL))
NYMPH = CardSubType("Nymph", (CREATURE, TRIBAL))
OCTOPUS = CardSubType("Octopus", (CREATURE, TRIBAL))
OGRE = CardSubType("Ogre", (CREATURE, TRIBAL))
OOZE = CardSubType("Ooze", (CREATURE, TRIBAL))
ORB = CardSubType("Orb", (CREATURE, TRIBAL))
ORC = CardSubType("Orc", (CREATURE, TRIBAL))
ORGG = CardSubType("Orgg", (CREATURE, TRIBAL))
OTTER = CardSubType("Otter", (CREATURE, TRIBAL))
OUPHE = CardSubType("Ouphe", (CREATURE, TRIBAL))
OX = CardSubType("Ox", (CREATURE, TRIBAL))
OYSTER = CardSubType("Oyster", (CREATURE, TRIBAL))
PANGOLIN = CardSubType("Pangolin", (CREATURE, TRIBAL))
PEASANT = CardSubType("Peasant", (CREATURE, TRIBAL))
PEGASUS = CardSubType("Pegasus", (CREATURE, TRIBAL))
PENTAVITE = CardSubType("Pentavite", (CREATURE, TRIBAL))
PERFORMER = CardSubType("Performer", (CREATURE, TRIBAL))
PEST = CardSubType("Pest", (CREATURE, TRIBAL))
PHELDDAGRIF = CardSubType("Phelddagrif", (CREATURE, TRIBAL))
PHOENIX = CardSubType("Phoenix", (CREATURE, TRIBAL))
PHYREXIAN = CardSubType("Phyrexian", (CREATURE, TRIBAL))
PILOT = CardSubType("Pilot", (CREATURE, TRIBAL))
PINCHER = CardSubType("Pincher", (CREATURE, TRIBAL))
PIRATE = CardSubType("Pirate", (CREATURE, TRIBAL))
PLANT = CardSubType("Plant", (CREATURE, TRIBAL))
PRAETOR = CardSubType("Praetor", (CREATURE, TRIBAL))
PRIMARCH = CardSubType("Primarch", (CREATURE, TRIBAL))
PRISM = CardSubType("Prism", (CREATURE, TRIBAL))
PROCESSOR = CardSubType("Processor", (CREATURE, TRIBAL))
RABBIT = CardSubType("Rabbit", (CREATURE, TRIBAL))
RACCOON = CardSubType("Raccoon", (CREATURE, TRIBAL))
RANGER = CardSubType("Ranger", (CREATURE, TRIBAL))
RAT = CardSubType("Rat", (CREATURE, TRIBAL))
REBEL = CardSubType("Rebel", (CREATURE, TRIBAL))
REFLECTION = CardSubType("Reflection", (CREATURE, TRIBAL))
RHINO = CardSubType("Rhino", (CREATURE, TRIBAL))
RIGGER = CardSubType("Rigger", (CREATURE, TRIBAL))
ROBOT = CardSubType("Robot", (CREATURE, TRIBAL))
ROGUE = CardSubType("Rogue", (CREATURE, TRIBAL))
SABLE = CardSubType("Sable", (CREATURE, TRIBAL))
SALAMANDER = CardSubType("Salamander", (CREATURE, TRIBAL))
SAMURAI = CardSubType("Samurai", (CREATURE, TRIBAL))
SAND = CardSubType("Sand", (CREATURE, TRIBAL))
SAPROLING = CardSubType("Saproling", (CREATURE, TRIBAL))
SATYR = CardSubType("Satyr", (CREATURE, TRIBAL))
SCARECROW = CardSubType("Scarecrow", (CREATURE, TRIBAL))
SCIENTIST = CardSubType("Scientist", (CREATURE, TRIBAL))
SCION = CardSubType("Scion", (CREATURE, TRIBAL))
SCORPION = CardSubType("Scorpion", (CREATURE, TRIBAL))
SCOUT = CardSubType("Scout", (CREATURE, TRIBAL))
SCULPTURE = CardSubType("Sculpture", (CREATURE, TRIBAL))
SERF = CardSubType("Serf", (CREATURE, TRIBAL))
SERPENT = CardSubType("Serpent", (CREATURE, TRIBAL))
SERVO = CardSubType("Servo", (CREATURE, TRIBAL))
SHADE = CardSubType("Shade", (CREATURE, TRIBAL))
SHAMAN = CardSubType("Shaman", (CREATURE, TRIBAL))
SHAPESHIFTER = CardSubType("Shapeshifter", (CREATURE, TRIBAL))
SHARK = CardSubType("Shark", (CREATURE, TRIBAL))
SHEEP = CardSubType("Sheep", (CREATURE, TRIBAL))
SIREN = CardSubType("Siren", (CREATURE, TRIBAL))
SKELETON = CardSubType("Skeleton", (CREATURE, TRIBAL))
SLITH = CardSubType("Slith", (CREATURE, TRIBAL))
SLIVER = CardSubType("Sliver", (CREATURE, TRIBAL))
SLUG = CardSubType("Slug", (CREATURE, TRIBAL))
SNAIL = CardSubType("Snail", (CREATURE, TRIBAL))
SNAKE = CardSubType("Snake", (CREATURE, TRIBAL))
SOLDIER = CardSubType("Soldier", (CREATURE, TRIBAL))
SOLTARI = CardSubType("Soltari", (CREATURE, TRIBAL))
SPAWN = CardSubType("Spawn", (CREATURE, TRIBAL))
SPECTER = CardSubType("Specter", (CREATURE, TRIBAL))
SPELLSHAPER = CardSubType("Spellshaper", (CREATURE, TRIBAL))
SPHINX = CardSubType("Sphinx", (CREATURE, TRIBAL))
SPIDER = CardSubType("Spider", (CREATURE, TRIBAL))
SPIKE = CardSubType("Spike", (CREATURE, TRIBAL))
SPIRIT = CardSubType("Spirit", (CREATURE, TRIBAL))
SPLINTER = CardSubType("Splinter", (CREATURE, TRIBAL))
SPONGE = CardSubType("Sponge", (CREATURE, TRIBAL))
SQUID = CardSubType("Squid", (CREATURE, TRIBAL))
SQUIRREL = CardSubType("Squirrel", (CREATURE, TRIBAL))
STARFISH = CardSubType("Starfish", (CREATURE, TRIBAL))
SURRAKAR = CardSubType("Surrakar", (CREATURE, TRIBAL))
SURVIVOR = CardSubType("Survivor", (CREATURE, TRIBAL))
TENTACLE = CardSubType("Tentacle", (CREATURE, TRIBAL))
TETRAVITE = CardSubType("Tetravite", (CREATURE, TRIBAL))
THALAKOS = CardSubType("Thalakos", (CREATURE, TRIBAL))
THOPTER = CardSubType("Thopter", (CREATURE, TRIBAL))
THRULL = CardSubType("Thrull", (CREATURE, TRIBAL))
TIEFLING = CardSubType("Tiefling", (CREATURE, TRIBAL))
TIMELORD = CardSubType("TimeLord", (CREATURE, TRIBAL))
TREEFOLK = CardSubType("Treefolk", (CREATURE, TRIBAL))
TRILOBITE = CardSubType("Trilobite", (CREATURE, TRIBAL))
TRISKELAVITE = CardSubType("Triskelavite", (CREATURE, TRIBAL))
TROLL = CardSubType("Troll", (CREATURE, TRIBAL))
TURTLE = CardSubType("Turtle", (CREATURE, TRIBAL))
TYRANID = CardSubType("Tyranid", (CREATURE, TRIBAL))
UNICORN = CardSubType("Unicorn", (CREATURE, TRIBAL))
VAMPIRE = CardSubType("Vampire", (CREATURE, TRIBAL))
VEDALKEN = CardSubType("Vedalken", (CREATURE, TRIBAL))
VIASHINO = CardSubType("Viashino", (CREATURE, TRIBAL))
VOLVER = CardSubType("Volver", (CREATURE, TRIBAL))
WALL = CardSubType("Wall", (CREATURE, TRIBAL))
WALRUS = CardSubType("Walrus", (CREATURE, TRIBAL))
WARLOCK = CardSubType("Warlock", (CREATURE, TRIBAL))
WARRIOR = CardSubType("Warrior", (CREATURE, TRIBAL))
WEIRD = CardSubType("Weird", (CREATURE, TRIBAL))
WEREWOLF = CardSubType("Werewolf", (CREATURE, TRIBAL))
WHALE = CardSubType("Whale", (CREATURE, TRIBAL))
WIZARD = CardSubType("Wizard", (CREATURE, TRIBAL))
WOLF = CardSubType("Wolf", (CREATURE, TRIBAL))
WOLVERINE = CardSubType("Wolverine", (CREATURE, TRIBAL))
WOMBAT = CardSubType("Wombat", (CREATURE, TRIBAL))
WORM = CardSubType("Worm", (CREATURE, TRIBAL))
WRAITH = CardSubType("Wraith", (CREATURE, TRIBAL))
WURM = CardSubType("Wurm", (CREATURE, TRIBAL))
YETI = CardSubType("Yeti", (CREATURE, TRIBAL))
ZOMBIE = CardSubType("Zombie", (CREATURE, TRIBAL))
ZUBERA = CardSubType("Zubera", (CREATURE, TRIBAL))


BASIC_LAND_TYPES = (
    PLAINS,
    ISLAND,
    SWAMP,
    MOUNTAIN,
    FOREST,
)

ALL_TYPES = tuple(
    member for name, member in inspect.getmembers(sys.modules[__name__]) if isinstance(member, BaseCardType)
)

ALL_TYPES_MAP = {
    member.name: member
    for name, member in inspect.getmembers(sys.modules[__name__])
    if isinstance(member, BaseCardType)
}


class TypeLine(object):
    SEPARATOR = " — "

    def __init__(self, *types: BaseCardType):
        self._types = frozenset(types)
        self._repr: t.Optional[str] = None

    def __eq__(self, other):
        return isinstance(other, TypeLine) and self._types == other.types

    def __lt__(self, other):
        return isinstance(other, TypeLine) and self._types < other.types

    def __le__(self, other):
        return isinstance(other, TypeLine) and self._types <= other.types

    def __gt__(self, other):
        return isinstance(other, TypeLine) and self._types > other.types

    def __ge__(self, other):
        return isinstance(other, TypeLine) and self._types >= other.types

    def __hash__(self):
        return hash(self._types)

    def __repr__(self):
        if self._repr is not None:
            return self._repr

        self._repr = " ".join(
            str(card_type)
            for card_type in itertools.chain(
                sorted(self.super_types),
                sorted(self.card_types),
            )
        )

        if self.sub_types:
            if self._repr:
                self._repr += TypeLine.SEPARATOR
            self._repr += " ".join(str(sub_type) for sub_type in sorted(self.sub_types))

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

    @property
    def is_permanent(self) -> bool:
        return any(t.is_permanent for t in self.card_types)
