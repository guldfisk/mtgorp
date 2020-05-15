import logging

from mtgorp.managejson.update import check_and_update


def mtgdb_init():
    logging.basicConfig(format = '%(levelname)s %(message)s', level = logging.INFO)
    check_and_update()


if __name__ == '__main__':
    mtgdb_init()
