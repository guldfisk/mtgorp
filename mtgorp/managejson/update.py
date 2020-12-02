import datetime
import functools
import logging
import typing as t
import os
import re

import requests as r

from xml.etree import ElementTree

import pickledb

from mtgorp.db import create
from mtgorp.managejson import download, paths


MTG_JSON_RSS_URL = 'http://mtgjson.com/atom.xml'
MTG_JSON_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def get_update_db():
    os.makedirs(paths.APP_DATA_PATH, exist_ok = True)
    return pickledb.load(paths.UPDATE_INFO_PATH, True, sig = False)


def with_update_db(f: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not 'update_db' in kwargs:
            kwargs['update_db'] = get_update_db()
        return f(*args, **kwargs)

    return wrapped


def check_rss(url: str = MTG_JSON_RSS_URL) -> t.Optional[datetime.datetime]:
    rg = r.get(url)
    root = ElementTree.fromstring(rg.text)

    for child in root:
        if re.match('.*updated$', child.tag):
            return datetime.datetime.strptime(child.text, MTG_JSON_DATETIME_FORMAT)

    return None


@with_update_db
def get_last_json_update(update_db: pickledb.PickleDB) -> t.Optional[datetime.datetime]:
    key = update_db.get('last_json_update')
    if not key:
        return None
    return datetime.datetime.strptime(key, MTG_JSON_DATETIME_FORMAT)


@with_update_db
def get_last_db_update(update_db: pickledb.PickleDB) -> t.Optional[datetime.datetime]:
    key = update_db.get('last_db_update')
    if not key:
        return None
    return datetime.datetime.strptime(key, MTG_JSON_DATETIME_FORMAT)


JUST_PICKLE = (create.update_pickle_database,)


@with_update_db
def regenerate_db(
    update_db: pickledb.PickleDB,
    force: bool = False,
    updaters: t.Sequence[t.Callable[[datetime.datetime], None]] = JUST_PICKLE,
) -> bool:
    last_json_update = get_last_json_update(update_db = update_db)
    last_db_update = get_last_db_update(update_db = update_db)

    if not last_db_update or last_db_update < last_json_update or force:
        logging.info('updating db')
        for updater in updaters:
            updater(last_json_update)
        update_db.set('last_db_update', last_json_update.strftime(MTG_JSON_DATETIME_FORMAT))
        logging.info('updated database')
        return True

    return False


@with_update_db
def check_and_update(
    update_db: pickledb.PickleDB,
    *,
    force: bool = False,
    force_json_download: bool = False,
    updaters: t.Sequence[t.Callable[[datetime.datetime], None]] = JUST_PICKLE,
) -> bool:
    last_remote_update = check_rss()
    if not last_remote_update and not force:
        return False

    last_json_update = get_last_json_update(update_db = update_db)

    outdated_json = not last_json_update or last_json_update < last_remote_update

    if outdated_json or force_json_download:
        logging.info('forced json download' if not outdated_json else 'mtgjson outdated')
        download.re_download()
        update_db.set('last_json_update', last_remote_update.strftime(MTG_JSON_DATETIME_FORMAT))
        logging.info('downloaded new json')
    else:
        logging.info('json up to date')

    return regenerate_db(update_db = update_db, force = force, updaters = updaters)


if __name__ == '__main__':
    check_and_update()
