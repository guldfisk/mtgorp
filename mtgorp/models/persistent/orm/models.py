from __future__ import annotations

import itertools
import typing as t

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from mtgorp.models import interfaces as i
from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.models.persistent.attributes.colors import Color
from mtgorp.models.persistent.attributes.expansiontype import ExpansionType
from mtgorp.models.persistent.attributes.flags import Flags
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.manacosts import ManaCost
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.models.persistent.attributes.typeline import TypeLine
from mtgorp.models.persistent.orm.fields.boosterkey import BoosterKeyField
from mtgorp.models.persistent.orm.fields.color import ColorField
from mtgorp.models.persistent.orm.fields.flags import FlagsField
from mtgorp.models.persistent.orm.fields.fragmentdividers import FragmentDividersField
from mtgorp.models.persistent.orm.fields.manacost import ManaCostField
from mtgorp.models.persistent.orm.fields.powertoughness import (
    PowerToughnessField,
    PTValueField,
)
from mtgorp.models.persistent.orm.fields.typeline import TypeLineField


class _Base(object):
    always_use_scoped_session = True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.primary_key})"


Base = declarative_base(cls=_Base)


class CardToCardboardFront(Base):
    __tablename__ = "card_to_cardboard_front"
    id = Column(Integer, primary_key=True)
    card_name = Column(String(255), ForeignKey("card.name", ondelete="CASCADE"))
    cardboard_name = Column(String(255), ForeignKey("cardboard.name", ondelete="CASCADE"))
    index = Column(Integer)

    @property
    def primary_key(self) -> int:
        return self.id


class CardToCardboardBack(Base):
    __tablename__ = "card_to_cardboard_back"
    id = Column(Integer, primary_key=True)
    card_name = Column(String(255), ForeignKey("card.name", ondelete="CASCADE"))
    cardboard_name = Column(String(255), ForeignKey("cardboard.name", ondelete="CASCADE"))
    index = Column(Integer)

    @property
    def primary_key(self) -> int:
        return self.id


class Card(Base, i.Card):
    __tablename__ = "card"

    name = Column(String(255), primary_key=True)

    type_line: TypeLine = Column(TypeLineField(255), nullable=False)
    mana_cost: ManaCost = Column(ManaCostField(255), nullable=True)
    color: t.AbstractSet[Color] = Column(ColorField(63), nullable=False)
    oracle_text = Column(Text, nullable=False)
    power_toughness = Column(PowerToughnessField(15), nullable=True)
    loyalty = Column(PTValueField(7), nullable=True)
    defense = Column(PTValueField(7), nullable=True)
    color_identity = Column(ColorField(63))

    front_cardboards = relationship(
        "Cardboard",
        secondary=CardToCardboardFront.__table__,
        back_populates="front_cards",
        cascade="all,delete",
    )

    back_cardboards = relationship(
        "Cardboard",
        secondary=CardToCardboardBack.__table__,
        back_populates="back_cards",
        cascade="all,delete",
    )

    @property
    def cardboards(self) -> t.FrozenSet[Cardboard]:
        return frozenset(itertools.chain(self.front_cardboards, self.back_cardboards))

    @property
    def primary_key(self) -> str:
        return self.name


class Cardboard(Base, i.Cardboard):
    __tablename__ = "cardboard"

    def __init__(
        self,
        front_cards: t.Sequence[Card],
        back_cards: t.Sequence[Card] = None,
        layout: Layout = Layout.STANDARD,
    ):
        self.front_cards = front_cards
        self.back_cards = back_cards
        self.layout = layout
        self.name = self.calc_name(
            c.name for c in itertools.chain(front_cards, back_cards if back_cards is not None else ())
        )

    name = Column(String(255), primary_key=True)

    front_cards = relationship(
        "Card",
        secondary=CardToCardboardFront.__table__,
        order_by=CardToCardboardFront.__table__.c.index,
        back_populates="front_cardboards",
        cascade="all,delete",
    )

    back_cards = relationship(
        "Card",
        secondary=CardToCardboardBack.__table__,
        order_by=CardToCardboardBack.__table__.c.index,
        back_populates="back_cardboards",
        cascade="all,delete",
    )

    printings = relationship("Printing", back_populates="cardboard", cascade="all, delete-orphan")

    layout = Column(Enum(Layout))

    @property
    def primary_key(self) -> str:
        return self.name


class Printing(i.Printing, Base):
    __tablename__ = "printing"

    def __init__(
        self,
        id: int,
        expansion: Expansion,
        cardboard: Cardboard,
        collector_number: int,
        collector_string: str,
        front_artist: Artist = None,
        front_flavor: str = None,
        back_artist: Artist = None,
        back_flavor: str = None,
        rarity: Rarity = None,
        in_booster: bool = True,
        flags: t.Optional[Flags] = None,
    ):
        self.id = id
        self.expansion = expansion
        self.cardboard = cardboard
        self.collector_number = collector_number
        self.collector_string = collector_string
        self.rarity = rarity
        self.in_booster = in_booster
        self.flags = flags
        self.front_face = Face(artist=front_artist, flavor=front_flavor)
        self.back_face = Face(artist=back_artist, flavor=back_flavor)

    id = Column(BigInteger, primary_key=True)

    cardboard_name = Column("Cardboard", ForeignKey("cardboard.name"))
    cardboard = relationship("Cardboard", back_populates="printings")

    expansion_name = Column(String(15), ForeignKey("expansion.code"))
    expansion = relationship("Expansion", back_populates="printings")

    collector_number = Column(Integer)
    collector_string = Column(Text())

    front_face_id = Column(Integer, ForeignKey("face.id"))
    front_face = relationship("Face", back_populates="front_owner", foreign_keys=[front_face_id])

    back_face_id = Column(Integer, ForeignKey("face.id"))
    back_face = relationship("Face", back_populates="back_owner", foreign_keys=[back_face_id])

    rarity = Column(Enum(Rarity))
    in_booster = Column(Boolean)
    flags = Column(FlagsField(255))

    @property
    def primary_key(self) -> int:
        return self.id


class Face(Base, i.Face):
    __tablename__ = "face"

    id = Column(Integer, primary_key=True)

    artist_name = Column(String(255), ForeignKey("artist.name"))
    artist = relationship("Artist", back_populates="faces")

    front_owner = relationship("Printing", foreign_keys=[Printing.front_face_id])
    back_owner = relationship("Printing", foreign_keys=[Printing.back_face_id])

    @property
    def owner(self) -> Printing:
        return self.front_owner or self.back_owner

    flavor = Column(Text)

    @property
    def primary_key(self) -> int:
        return self.id


class Artist(Base, i.Artist):
    __tablename__ = "artist"

    name = Column(String(255), primary_key=True)

    faces = relationship("Face", back_populates="artist", cascade="all, delete-orphan")

    @property
    def primary_key(self) -> t.Union[str, int]:
        return self.name


class Block(Base, i.Block):
    __tablename__ = "block"
    name = Column(String(255), primary_key=True)

    expansions = relationship("Expansion", back_populates="block")

    @property
    def primary_key(self) -> str:
        return self.name


class Expansion(Base, i.Expansion):
    __tablename__ = "expansion"

    code = Column(String(15), primary_key=True)
    name = Column(String(255))

    block_name = Column(String(255), ForeignKey("block.name"))
    block = relationship("Block", back_populates="expansions")

    printings = relationship("Printing", back_populates="expansion")

    fragment_dividers = Column(FragmentDividersField(15))

    expansion_type = Column(Enum(ExpansionType))

    release_date = Column(DateTime)

    booster_key = Column(BoosterKeyField)

    main_code = Column(String(15), ForeignKey("expansion.code"), nullable=True)
    main = relationship("Expansion", foreign_keys=[main_code])

    basics_code = Column(String(15), ForeignKey("expansion.code"), nullable=True)
    basics = relationship("Expansion", foreign_keys=[basics_code])

    premium_code = Column(String(15), ForeignKey("expansion.code"), nullable=True)
    premium = relationship("Expansion", foreign_keys=[premium_code])

    @property
    def booster_expansion_collection(self) -> t.Optional[i.ExpansionCollection]:
        if any((self.main, self.basics, self.premium)):
            return i.ExpansionCollection(self.main, self.basics, self.premium)

    border = Column(Enum(Border))

    magic_card_info_code = Column(String(15))
    mkm_name = Column(String(255))
    mkm_id = Column(Integer)

    @property
    def primary_key(self) -> str:
        return self.code


def create(engine: Engine):
    Base.metadata.create_all(engine)
