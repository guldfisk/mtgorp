import os
import re
import xml.etree.ElementTree as ET

import requests as r

from managejson import download, fix
from resourceload import cardload


class MTGJsonHome(object):
	url = 'http://mtgjson.com/atom.xml'

def check_rss(url):
	rg = r.get(url)
	root = ET.fromstring(rg.text)
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
	
def check_and_update():
	last_updates = check_rss(MTGJsonHome.url)
	print(last_updates)
	if not last_updates:
		return False
	if not os.path.exists(os.path.join(cardload.path)):
		os.makedirs(cardload.path)
	open(os.path.join(cardload.path, 'lastupdtd.txt'), 'a').close()
	with open(os.path.join(cardload.path, 'lastupdtd.txt'), 'r+') as f:
		value = f.read()
		print(value)
		if last_updates!=value:
			print('updating')
			update()
			download.delete_content(f)
			f.write(last_updates)
			return True
		return False

if __name__=='__main__':
	check_and_update()