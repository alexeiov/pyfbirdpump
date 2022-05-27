import time
import config
from connection import db_connect


def cond_update(data_update: dict, db: str = config.address_azot) -> None:
    start_time = time.time()

    c = db_connect(db)
    cur = c.cursor()

    # update_statement = cur.prep(config.data_update_req_usd_rate)
    update_statement_1 = cur.prep(config.data_update_req_trend_me_spec)

    cur.execute(config.data_get_req_1) # Base data request should not be changed in most cases
    # print(cur)

    updated_data = {}

    for line in cur.fetchall():
        # print(line)
        for key, data in data_update.items(): # Standart structure of the data for conditional upload to table: two columns, 1st - key, 2nd - data
            # if key == line[1]:
            if key == line[3] and line[1] not in ('1', '2', '3'):
            # if key == line[3]:
            #     print(line)
                # cur.execute(update_statement_1, (data, key))
                updated_data[line[0]] = data

    # print(updated_data)

    for key, data in updated_data.items():
        cur.execute(update_statement_1, (data, key))

    c.commit()
    c.close()
    print(f'conditional data pump completed, execution time: {round(time.time() - start_time, 0)} seconds')

    # TODO: add requests and source files logging
