import datetime
import typing as t
from abc import abstractmethod

from orp.database import OrpDatabase, OrpTable, PickleDatabase, PickleTable
from orp.sql import SqlDatabase, SqlTable
from sqlalchemy import Column, DateTime, Integer, LargeBinary, MetaData, Table, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from mtgorp.models import interfaces as i
from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.block import Block
from mtgorp.models.persistent.card import Card
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.models.persistent.orm import models as models
from mtgorp.models.persistent.printing import Printing


class CardDatabase(OrpDatabase):
    _cards: OrpTable[str, i.Card]
    _cardboards: OrpTable[str, i.Cardboard]
    _printings: OrpTable[int, i.Printing]
    _artists: OrpTable[str, i.Artist]
    _blocks: OrpTable[str, i.Block]
    _expansions: OrpTable[str, i.Expansion]

    @property
    def cards(self) -> OrpTable[str, i.Card]:
        return self._cards

    @property
    def cardboards(self) -> OrpTable[str, i.Cardboard]:
        return self._cardboards

    @property
    def printings(self) -> OrpTable[int, i.Printing]:
        return self._printings

    @property
    def artists(self) -> OrpTable[str, i.Artist]:
        return self._artists

    @property
    def blocks(self) -> OrpTable[str, i.Block]:
        return self._blocks

    @property
    def expansions(self) -> OrpTable[str, i.Expansion]:
        return self._expansions

    @property
    @abstractmethod
    def json_version(self) -> datetime.datetime:
        pass


DB = t.TypeVar("DB", bound=CardDatabase)


class PickleCardDatabase(PickleDatabase, CardDatabase):
    def __init__(
        self,
        cards: PickleTable[str, Card],
        cardboards: PickleTable[str, Cardboard],
        printings: PickleTable[int, Printing],
        artists: PickleTable[str, Artist],
        blocks: PickleTable[str, Block],
        expansions: PickleTable[str, Expansion],
        json_version: datetime.datetime,
        created_at: datetime.datetime,
    ):
        super().__init__(
            {
                i.Card: cards,
                i.Cardboard: cardboards,
                i.Printing: printings,
                i.Artist: artists,
                i.Block: blocks,
                i.Expansion: expansions,
            },
            created_at,
        )
        self._json_version = json_version

        self._cards = cards
        self._cardboards = cardboards
        self._printings = printings
        self._artists = artists
        self._blocks = blocks
        self._expansions = expansions

    @property
    def json_version(self) -> datetime.datetime:
        return self._json_version


metadata = MetaData()

meta_info = Table(
    "meta",
    metadata,
    Column("version", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("checksum", LargeBinary(256)),
    Column("json_version", DateTime),
)


class SqlCardDatabase(SqlDatabase, CardDatabase):
    def __init__(
        self,
        cards: SqlTable[str, models.Card],
        cardboards: SqlTable[str, models.Cardboard],
        printings: SqlTable[int, models.Printing],
        artists: SqlTable[str, models.Artist],
        blocks: SqlTable[str, models.Block],
        expansions: SqlTable[str, models.Expansion],
        engine: Engine,
    ):
        super().__init__(
            {
                i.Card: cards,
                i.Cardboard: cardboards,
                i.Printing: printings,
                i.Artist: artists,
                i.Block: blocks,
                i.Expansion: expansions,
            },
            engine,
        )

        self._cards = cards
        self._cardboards = cardboards
        self._printings = printings
        self._artists = artists
        self._blocks = blocks
        self._expansions = expansions

    @property
    def json_version(self) -> datetime.datetime:
        with self._engine.connect() as connection:
            return connection.execute(
                select([meta_info.c.json_version]).order_by(meta_info.c.version.desc()).limit(1)
            ).fetchone()[0]

    def probe(self, session: Session) -> bool:
        return session.query(models.Printing.id).first()
