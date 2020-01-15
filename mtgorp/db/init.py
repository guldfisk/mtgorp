from mtgorp.db import create

from mtgorp.managejson import download
from mtgorp.managejson.update import check, update_last_updated


def mtgdb_init():
    last_updates = check()
    if last_updates is not None:
        print('New magic json')
        download.re_download()
        print('New magic json downloaded')
        create.update_database()
        print('Database updated')
        update_last_updated(last_updates)
    else:
        print('Magic db up to date')


if __name__ == '__main__':
    mtgdb_init()
