from mtgorp.db.create import CardDatabase
from mtgorp.db.load import Loader


class MtgDb(object):
    db: CardDatabase = None

    @classmethod
    def init(cls):
        cls.db = Loader.load()
