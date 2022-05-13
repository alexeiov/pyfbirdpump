import psycopg2 as ps2
import config
from connection import db_connect


def get_fb_data(connection):
    data = []
    c = connection
    cur = c.cursor()
    cur.execute(config.data_get_for_ps)
    for line in cur.fetchall():
        data.append(line)
    c.close()
    return data


def pg_upload(data):
    conn_pg = ps2.connect(config.address_pg)
    cur = conn_pg.cursor()
    # cur.execute('SELECT version()')
    # db_version = cur.fetchone()
    # print(db_version)

    insert_statement = config.data_pump_req_ps

    counts = 0
    for row in data:
        print(row)
        cur.execute(insert_statement, row)
        counts += 1
        print(counts)

    conn_pg.commit()
    cur.close()
    conn_pg.close()


data_fb = get_fb_data(db_connect())
pg_upload(data_fb)
