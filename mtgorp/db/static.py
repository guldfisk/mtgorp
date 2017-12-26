from mtgorp.db.create import CardDatabase
from mtgorp.db.load import Loader

class MtgDb(object):
	db = None #type: CardDatabase
	def init(self):
		self.db = Loader.load()