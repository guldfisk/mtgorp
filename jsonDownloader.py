#Handles redownlosd from mtgsjon

import requests as r

def downloadFileBytes(url, chunkSize = 1024):
	ro = r.get(url, stream=True)
	b = b''
	for chunk in ro.iter_content(chunk_size=chunkSize):
		b+=chunk
	return(b)
			
def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
	
toRetrieve = {'allCards': 'http://mtgjson.com/json/AllCards.json', 'allSets': 'http://mtgjson.com/json/AllSets.json'}

#Downloads toRetrieve and writes to file	
def makeNew(toRetrieve):
	for key in toRetrieve:
		bjson = downloadFileBytes(toRetrieve[key])
		open(key+'.json', 'wb').write(bjson)

def reDownload():
	makeNew(toRetrieve)

if __name__=='__main__': reDownload()