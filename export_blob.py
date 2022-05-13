import time
import config
from connection import db_connect
from pathlib import Path


def get_blob():
    start_time = time.time()

    c = db_connect()
    cur = c.cursor()

    id_mt = int(input('Enter Main Tab ID:'))
    save_path = input('Enter save path: ')

    blob_statement = cur.prep(config.blob_get_photo)
    cur.execute(blob_statement, (id_mt,))
    data_f = cur.fetchone()

    try:
        pic = data_f[0].read()
        asset_name = data_f[2].replace('\\', '_').replace('/', '_')
        pic_name = Path(save_path).joinpath(f'{data_f[1]}_-_{asset_name}.jpg')

        with open(pic_name, 'wb') as d_f:
            d_f.write(pic)
        print(f'Photo saved to the folder {save_path}')
    except AttributeError:
        print("Error: There is no photo for the item with this ID in the technical data table")
    except TypeError:
        print("Error: There is no item with this ID in the technical data table")
    except (FileNotFoundError, OSError):
        print('Error: can not process asset name')
    # print(d)
        # print('test')

    c.commit()
    c.close()


get_blob()
