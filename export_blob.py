import time
import config
from connection import db_connect


def get_blob():
    start_time = time.time()

    c = db_connect()
    cur = c.cursor()
    cur.execute(config.blob_get_photo)
    data_f = cur.fetchone()
    pic = data_f[0].read()
    pic_name = f'{data_f[1]}.jpg'

    with open(pic_name, 'wb') as d_f:
        d_f.write(pic)
    # print(d)
        # print('test')

    c.commit()
    c.close()


get_blob()
