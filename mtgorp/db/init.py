from mtgorp.managejson.update import check_and_update
from mtgorp.db.create import update_database


def mtgdb_init():
    if check_and_update():
        print('New magic json')
        update_database()
        print('Database updated')
    else:
        print('Magic db up to date')


if __name__ == '__main__':
    mtgdb_init()
