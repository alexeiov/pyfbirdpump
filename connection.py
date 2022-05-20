import fdb
import config


def db_connect(db: str = config.address_azot):
    con = fdb.connect(dsn=db, user=config.username, password=config.passwd,
                      charset='win1251')
    return con


if __name__ == 'main':
    db_connect()
