import typing as t
import os
from pickle import UnpicklingError
from abc import abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from orp.persist import PicklePersistor

from mtgorp.managejson import paths
from mtgorp.db.database import DB, PickleCardDatabase, SqlCardDatabase
from mtgorp.models.persistent.orm import models as sql_models
from orp.sql import SqlTable


DB_PATH = os.path.join(paths.APP_DATA_PATH, 'db')


class DBLoadException(Exception):
    pass


class Loader(t.Generic[DB]):

    @abstractmethod
    def load(self) -> DB:
        pass


class PickleLoader(Loader[PickleCardDatabase]):

    def load(self) -> PickleCardDatabase:
        try:
            return PicklePersistor(
                os.path.join(paths.APP_DATA_PATH, 'db')
            ).load()
        except (FileNotFoundError, EOFError, UnpicklingError):
            raise DBLoadException()


class SqlLoader(Loader[SqlCardDatabase]):

    def __init__(self, engine: Engine, session_factory: t.Callable[[], Session]):
        self._session_factory = session_factory
        self._engine = engine

    def load(self) -> SqlCardDatabase:
        return SqlCardDatabase(
            cards = SqlTable(sql_models.Card, self._session_factory),
            cardboards = SqlTable(sql_models.Cardboard, self._session_factory),
            printings = SqlTable(sql_models.Printing, self._session_factory),
            artists = SqlTable(sql_models.Artist, self._session_factory),
            blocks = SqlTable(sql_models.Block, self._session_factory),
            expansions = SqlTable(sql_models.Expansion, self._session_factory),
            engine = self._engine,
        )
