import traceback

from trends_import import get_av_rub_rates
import config
from connection import db_connect
import time


def insert_rates(db):
    c = db_connect(db)
    cur = c.cursor()

    try:
        start_time = time.time()
        num_insert_type = int(input('Enter insert type number:'))
        curr = input('Enter currency:')
        start_date = input('Enter start date:')
        finish_date = input('Enter finish date:')
        # curr_code_to_db = 0 if curr == 'R01235' else 2
        data_to_insert = get_av_rub_rates(config.cbr_currency_codes[curr][0], start_date, finish_date)
        insert_statement = cur.prep(config.data_insert_reqs[num_insert_type])
        for key, data in data_to_insert.items():
            cur.execute(insert_statement, (key, data, config.cbr_currency_codes[curr][1], ))
        c.commit()
        c.close()

    except Exception:
        traceback.print_exc()

    finally:
        c.close()


def update_prev_trends(db):
    c = db_connect(db)
    cur = c.cursor()

    try:
        start_time = time.time()
        num_update_type = int(input('Enter update type number:'))
        # data_to_insert = get_av_rub_rates(config.cbr_currency_codes[curr][0], start_date, finish_date)
        # insert_statement = cur.prep(config.data_update_reqs[num_update_type])
        # for key, data in data_to_insert.items():
        #     cur.execute(insert_statement, (key, data, config.cbr_currency_codes[curr][1], ))
        c.commit()
        c.close()

    except Exception:
        traceback.print_exc()

    finally:
        c.close()


if __name__ == '__main__':
    insert_rates(config.db_addresses['kva_6']) # date format: dd/mm/yyyy
    # update_prev_trends(config.db_addresses['kva_5'])
