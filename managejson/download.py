import os
import requests as r

from resourceload.locate import Locator

PATH = os.path.join(Locator.path, 'jsons')
ALL_CARDS_PATH = os.path.join(PATH, 'allCards' + '.json')
ALL_SETS_PATH = os.path.join(PATH, 'allSets' + '.json')

if not os.path.exists(Locator.path):
	os.makedirs(PATH)

def download_file_bytes(url, location, chunk_size = 1024):
	ro = r.get(url, stream=True)
	with open(location, 'wb') as f:
		for chunk in ro.iter_content(chunk_size=chunk_size):
			f.write(chunk)

TO_RETRIEVE = {
	ALL_CARDS_PATH: 'http://mtgjson.com/json/AllCards.json',
	ALL_SETS_PATH: 'http://mtgjson.com/json/AllSets.json'
}

#Downloads toRetrieve and writes to file
def make_new(to_retrieve):
	for path in to_retrieve:
		download_file_bytes(
			to_retrieve[path],
			path
		)

def re_download():
	make_new(TO_RETRIEVE)

if __name__=='__main__':
	re_download()