import fdb
import config


def db_connect():
    con = fdb.connect(dsn=config.address_azot, user=config.username, password=config.passwd,
                      charset='win1251')
    return con


if __name__ == 'main':
    db_connect()
