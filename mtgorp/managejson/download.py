import os
import requests as r

import mtgorp.managejson.paths as paths

def download_file_bytes(url, location, chunk_size = 1024):
	ro = r.get(url, stream=True)
	with open(location, 'wb') as f:
		for chunk in ro.iter_content(chunk_size=chunk_size):
			f.write(chunk)

TO_RETRIEVE = {
	paths.ALL_CARDS_PATH: 'http://mtgjson.com/json/AllCards.json',
	paths.ALL_SETS_PATH: 'http://mtgjson.com/json/AllSets.json'
}

def make_new(to_retrieve):
	for path in to_retrieve:
		download_file_bytes(
			to_retrieve[path],
			path
		)

def re_download():
	if not os.path.exists(paths.JSON_PATH):
		os.makedirs(paths.JSON_PATH)
	make_new(TO_RETRIEVE)

if __name__=='__main__':
	re_download()