import mtgjsonHome
import jsonDownloader
import mtgUtility
import requests as r
import xml.etree.ElementTree as ET
import re

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
	mtgUtility.makeCardsFixed()
	mtgUtility.makeSetsFixed()
	
def checkAndUpdate():
	lastup = checkRSS(mtgjsonHome.url)
	if not lastup:
		print('Could not retrieve last update')
		return(None)
	open('lastupdtd.txt', 'a').close()
	file = open('lastupdtd.txt', 'r+')
	currentVersion = file.read()
	print('Current version', currentVersion, '\nLast updated', lastup)
	if lastup!=currentVersion:
		print('Redownloading')
		updt()
		print('Updating current version string')
		jsonDownloader.deleteContent(file)
		file.write(lastup)
	file.close()

if __name__=='__main__': checkAndUpdate()