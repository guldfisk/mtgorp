import datetime
import os
import sys
import typing as t

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from orp.persist import PicklePersistor
from orp.sql import SqlTable
from orp.database import OrpTable, PickleTable, O as _O, M as _M

from mtgorp.db.database import PickleCardDatabase, SqlCardDatabase, metadata, meta_info
from mtgorp.db.parse import DatabaseCreator
from mtgorp.managejson import paths
from mtgorp.models.interfaces import MtgModel
from mtgorp.models.persistent.artist import Artist
from mtgorp.models.persistent.block import Block
from mtgorp.models.persistent.card import Card
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.models.persistent.printing import Printing
from mtgorp.models import interfaces as i
from mtgorp.models.persistent.orm import models as models


class PickleDatabaseCreator(DatabaseCreator[PickleCardDatabase]):
    _model_parser_map = {
        i.Artist: Artist,
        i.Card: Card,
        i.Cardboard: Cardboard,
        i.Expansion: Expansion,
        i.Printing: Printing,
        i.Block: Block,
    }

    def create_table_for_model(self, model: t.Type[MtgModel]) -> OrpTable:
        return PickleTable()

    def _create_database_from_tables(self, tables: t.MutableMapping[str, OrpTable[_O, _M]]) -> PickleCardDatabase:
        tables['cardboards'] = PickleTable(
            {
                pk: cardboard
                for pk, cardboard in
                tables['cardboards'].items()
                if cardboard.printings
            }
        )

        return PickleCardDatabase(
            **tables,
            created_at = datetime.datetime.now(),
            json_version = datetime.datetime.now(),
        )


class SqlDatabaseCreator(DatabaseCreator[SqlCardDatabase]):
    _model_parser_map = {
        i.Artist: models.Artist,
        i.Card: models.Card,
        i.Cardboard: models.Cardboard,
        i.Expansion: models.Expansion,
        i.Printing: models.Printing,
        i.Block: models.Block,
    }

    def __init__(
        self,
        session_factory: t.Callable[[], Session],
        engine: Engine,
        json_updated_at: datetime.datetime,
        *,
        all_cards_path: str = paths.ALL_CARDS_PATH,
        all_sets_path: str = paths.ALL_SETS_PATH,
    ):
        super().__init__(json_updated_at, all_cards_path = all_cards_path, all_sets_path = all_sets_path)
        self._session_factory = session_factory
        self._engine = engine

    def create_table_for_model(self, model: t.Type[MtgModel]) -> OrpTable:
        return SqlTable(model, self._session_factory)

    def _pre_run(self) -> None:
        models.Base.metadata.drop_all(self._engine)
        models.Base.metadata.create_all(self._engine)

    def _create_database_from_tables(self, tables: t.MutableMapping[str, OrpTable[_O, _M]]) -> SqlCardDatabase:
        session = self._session_factory()
        database = SqlCardDatabase(
            **tables,
            engine = self._engine,
        )
        metadata.drop_all(self._engine)
        metadata.create_all(self._engine)
        session.query(models.Cardboard).filter(~models.Cardboard.printings.any()).delete(synchronize_session = False)

        with self._engine.connect() as connection:
            connection.execute(
                meta_info.insert(),
                created_at = datetime.datetime.now(),
                json_version = self._json_updated_at,
                checksum = database.calc_checksum(),
            )
        session.commit()
        return database


def get_sql_database_updater(
    session_factory: t.Callable[[], Session],
    engine: Engine,
    all_cards_path = paths.ALL_CARDS_PATH,
    all_sets_path = paths.ALL_SETS_PATH,
) -> t.Callable[[datetime.datetime], SqlCardDatabase]:
    def update_sql_database(
        json_updated_at: t.Optional[datetime.datetime] = None,
    ) -> SqlCardDatabase:
        return SqlDatabaseCreator(
            session_factory = session_factory,
            engine = engine,
            json_updated_at = datetime.datetime.fromtimestamp(0) if json_updated_at is None else json_updated_at,
            all_cards_path = all_cards_path,
            all_sets_path = all_sets_path,
        ).create_database()

    return update_sql_database


def update_pickle_database(
    json_updated_at: t.Optional[datetime.datetime] = None,
    all_cards_path = paths.ALL_CARDS_PATH,
    all_sets_path = paths.ALL_SETS_PATH,
    db_path = paths.APP_DATA_PATH,
) -> PickleCardDatabase:
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    db = PickleDatabaseCreator(
        datetime.datetime.fromtimestamp(0) if json_updated_at is None else json_updated_at,
        all_cards_path = all_cards_path,
        all_sets_path = all_sets_path,
    ).create_database()

    previous_recursion_limit = sys.getrecursionlimit()

    temp_path = os.path.join(paths.APP_DATA_PATH, '_db')

    try:
        sys.setrecursionlimit(2 ** 16)
        PicklePersistor(temp_path).save(db)
    finally:
        sys.setrecursionlimit(previous_recursion_limit)

    os.rename(temp_path, os.path.join(paths.APP_DATA_PATH, 'db'))

    return db


if __name__ == '__main__':
    update_pickle_database()
