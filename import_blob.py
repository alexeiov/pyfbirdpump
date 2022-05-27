import config
from connection import db_connect
import time
from pathlib import Path


class PhotoExists(Exception):
    pass


def set_blob():
    try:
        start_time = time.time()
        open_path = input('Enter path to file:')
        photo_to_add_main = input('Enter general view photo filename:')
        photo_to_add_plate = input('Enter plate photo filename:')

        filename_os = Path(open_path).joinpath(photo_to_add_main)
        filename_plate = Path(open_path).joinpath(photo_to_add_plate)

        with open (filename_os, 'rb') as d_f:
            main_ph = d_f.read()

        if photo_to_add_plate:
            with open (filename_plate, 'rb') as d_f_p:
                plate_ph = d_f_p.read()
        else:
            plate_ph = None

        # inv = '066581_ОС'
        # os_name = 'ПАРОВАЯ ТУРБИНА №5 ВД ПР-25-90'

        trans_type = int(input('Enter transaction type (1 - for new record, 2 - for adding photo to existing record): '))

        id_mt = int(input('Enter Main Tab ID:'))

        c = db_connect()
        cur = c.cursor()
        st_check_blob = cur.prep(config.data_get_check_blob)
        cur.execute(st_check_blob, (id_mt,))
        check_blob = cur.fetchall()
        # for k in check_blob:
        #     print(k)
        c.commit()
        c.close()

        c = db_connect()
        cur = c.cursor()

        if not check_blob:
            if trans_type == 1:
                inv = input('Enter inventory number:')
                subdiv_name = input('Enter subdiv_name:')
                os_name = input('Enter asset name:')
                aar_gr = input('Enter asset group:')
                tech_pos = input('Enter technical position index: ')
                blob_statement = cur.prep(config.blob_set_photo)
                cur.execute(blob_statement, (inv, id_mt, aar_gr, os_name, subdiv_name, main_ph, plate_ph, tech_pos,))
            elif trans_type == 2:
                blob_statement = cur.prep(config.blob_set_photo_exist)
                cur.execute(blob_statement, (main_ph, id_mt,))
        else:
            raise PhotoExists

        c.commit()
        c.close()

    except PhotoExists:
        print('This item already has a photo')


set_blob()
