import os

from orp.persist import PicklePersistor

from mtgorp.managejson import paths
from mtgorp.db.create import CardDatabase

DB_PATH = os.path.join(paths.APP_DATA_PATH, 'db')

class Loader(object):
	@staticmethod
	def load() -> CardDatabase:
		return PicklePersistor(
			os.path.join(paths.APP_DATA_PATH, 'db')
		).load()
