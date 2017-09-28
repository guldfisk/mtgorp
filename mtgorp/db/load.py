import os

from orp.persist import PicklePersistor

from mtgorp.managejson import paths

DB_PATH = os.path.join(paths.APP_DATA_PATH, 'db')

class Loader(object):
	@staticmethod
	def load():
		return PicklePersistor(
			os.path.join(paths.APP_DATA_PATH, 'db')
		).load()
