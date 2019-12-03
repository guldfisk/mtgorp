import os

from orp.persist import PicklePersistor

from mtgorp.managejson import paths
from mtgorp.db.create import CardDatabase


DB_PATH = os.path.join(paths.APP_DATA_PATH, 'db')


class DBLoadException(Exception):
    pass


class Loader(object):

    @classmethod
    def load(cls) -> CardDatabase:
        try:
            return PicklePersistor(
                os.path.join(paths.APP_DATA_PATH, 'db')
            ).load()
        except FileNotFoundError:
            raise DBLoadException()
