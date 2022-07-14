import traceback

from trends_import import get_av_rub_rates
import config
from connection import db_connect
import time


def insert_trends(db):
    c = db_connect(db)
    cur = c.cursor()

    try:
        start_time = time.time()
        num_insert_type = int(input('Enter insert type number:'))
        curr_code = input('Enter currency code:')
        start_date = input('Enter start date:')
        finish_date = input('Enter finish date:')
        curr_code_to_db = 0 if curr_code == 'R01235' else 2
        data_to_insert = get_av_rub_rates(curr_code, start_date, finish_date)
        insert_statement = cur.prep(config.data_insert_reqs[num_insert_type])
        for key, data in data_to_insert.items():
            cur.execute(insert_statement, (key, data, curr_code_to_db, ))
        c.commit()
        c.close()

    except Exception:
        traceback.print_exc()

    finally:
        c.close()


if __name__ == '__main__':
    insert_trends(config.db_addresses['kva_5'])
