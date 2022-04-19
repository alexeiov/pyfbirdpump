import config
from connection import db_connect
import time


def set_blob():
    start_time = time.time()
    filename = '2022-04-14 10-14-08.JPG'
    with open (filename, 'rb') as d_f:
        data_ph = d_f.read()
    inv = '066581_ОС'
    os_name = 'ПАРОВАЯ ТУРБИНА №5 ВД ПР-25-90'
    c = db_connect()
    cur = c.cursor()
    blob_statement = cur.prep(config.blob_set_photo)
    cur.execute(blob_statement, (inv, os_name, data_ph))
    c.commit()
    c.close()


set_blob()
