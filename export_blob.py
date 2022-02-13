import time
import config
from connection import db_connect


def get_blob():
    start_time = time.time()

    c = db_connect()
    cur = c.cursor()
    cur.execute(config.blob_get)
    data_f = cur.fetchall()

    for d in data_f:
        with open('from_blob.txt', 'w', encoding='utf8') as d_f:
            d_f.writelines(d)
        # print(d)
        # print('test')

    c.commit()
    c.close()


get_blob()
