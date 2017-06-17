import os

import requests as r

from resourceload import cardload


def download_file_bytes(url, chunk_size = 1024):
	ro = r.get(url, stream=True)
	bs = b''
	for chunk in ro.iter_content(chunk_size=chunk_size):
		bs+=chunk
	return bs
			
def delete_content(f):
	f.seek(0)
	f.truncate()
	
to_retrieve = {
	'allCards': 'http://mtgjson.com/json/AllCards.json',
	'allSets': 'http://mtgjson.com/json/AllSets.json'
}

#Downloads toRetrieve and writes to file	
def make_new(to_retrieve):
	if not os.path.exists(cardload.path):
		os.makedirs(cardload.path)
	for key in to_retrieve:
		bs = download_file_bytes(to_retrieve[key])
		with open(os.path.join(cardload.path, key+ '.json'), 'wb') as f:
			f.write(bs)

def re_download():
	make_new(to_retrieve)

if __name__=='__main__':
	re_download()