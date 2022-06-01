import fdb
import config


def db_connect(db: str):
    con = fdb.connect(dsn=db, user=config.username, password=config.passwd,
                      charset='win1251')
    return con


if __name__ == 'main':
    db_connect()
