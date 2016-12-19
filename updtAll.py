import jsonDownloader
import mtgJsonFix
import requests as r
import xml.etree.ElementTree as ET
import re
import os

class MTGJsonHome(object):
	url = 'http://mtgjson.com/atom.xml'

def checkRSS(url):
	rg = r.get(url)
	root = ET.fromstring(rg.text)
	lastup = None
	for child in root:
		if re.match('.*updated$', child.tag):
			lastup = child.text
			break
	return(lastup)

def updt():
	jsonDownloader.reDownload()
	mtgJsonFix.makeCardsFixed()
	mtgJsonFix.makeSetsFixed()
	
def checkAndUpdate():
	lastup = checkRSS(MTGJsonHome.url)
	if not lastup:
		print('Could not retrieve last update')
		return None
	open(os.path.join('resources', 'lastupdtd.txt'), 'a').close()
	file = open(os.path.join('resources', 'lastupdtd.txt'), 'r+')
	currentVersion = file.read()
	print('Current version', currentVersion, '\nLast updat	ed', lastup)
	if lastup!=currentVersion:
		print('Redownloading')
		updt()
		print('Updating current version string')
		jsonDownloader.deleteContent(file)
		file.write(lastup)
	file.close()

if __name__=='__main__': checkAndUpdate()