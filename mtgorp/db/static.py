from mtgorp.db.create import CardDatabase
from mtgorp.db.load import Loader

class MtgDb(object):
	db = None #type: CardDatabase
	@classmethod
	def init(cls):
		cls.db = Loader.load()