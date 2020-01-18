import typing as t

import os
import re

import requests as r

from xml.etree import ElementTree

from mtgorp.db import create

from mtgorp.managejson import download, paths


MTG_JSON_RSS_URL = 'http://mtgjson.com/atom.xml'


def check_rss(url) -> t.Optional[str]:
    rg = r.get(url)
    root = ElementTree.fromstring(rg.text)
    last_updates = None

    for child in root:
        if re.match('.*updated$', child.tag):
            last_updates = child.text
            break

    return last_updates


def update() -> None:
    download.re_download()
    create.update_database()


def delete_content(f) -> None:
    f.seek(0)
    f.truncate()
    
    
def check() -> t.Optional[str]:
    last_updates = check_rss(MTG_JSON_RSS_URL)

    if not last_updates:
        return None

    if not os.path.exists(paths.JSON_PATH):
        os.makedirs(paths.JSON_PATH)

    open(os.path.join(paths.JSON_PATH, 'lastupdtd.txt'), 'a').close()
    
    with open(os.path.join(paths.JSON_PATH, 'lastupdtd.txt'), 'r') as f:
        return None if last_updates == f.read() else last_updates
    

def update_last_updated(last_updated: str) -> None:
    with open(os.path.join(paths.JSON_PATH, 'lastupdtd.txt'), 'w') as f:
        f.write(last_updated)


def check_and_update() -> bool:
    last_updates = check()
    if last_updates is not None:
        update()
        update_last_updated(last_updates)
        return True
    return False


if __name__ == '__main__':
    check_and_update()
