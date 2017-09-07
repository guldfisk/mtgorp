import os
import re

import requests as r

from xml.etree import ElementTree
from managejson import download, fix

class MTGJsonHome(object):
	url = 'http://mtgjson.com/atom.xml'

def check_rss(url):
	rg = r.get(url)
	root = ElementTree.fromstring(rg.text)
	last_updates = None
	for child in root:
		if re.match('.*updated$', child.tag):
			last_updates = child.text
			break
	return last_updates

def update():
	download.re_download()
	fix.make_cards_fixed()
	fix.make_sets_fixed()

def delete_content(f):
	f.seek(0)
	f.truncate()

def check_and_update():
	last_updates = check_rss(MTGJsonHome.url)
	print(last_updates)
	if not last_updates:
		return False
	open(os.path.join(download.PATH, 'lastupdtd.txt'), 'a').close()
	with open(os.path.join(download.PATH, 'lastupdtd.txt'), 'r+') as f:
		value = f.read()
		print(value)
		if last_updates!=value:
			print('updating')
			update()
			delete_content(f)
			f.write(last_updates)
			return True
		return False

if __name__=='__main__':
	check_and_update()