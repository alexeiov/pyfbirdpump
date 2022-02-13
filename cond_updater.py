import time
import config
from connection import db_connect


def cond_update(data_update):
    start_time = time.time()

    c = db_connect()
    cur = c.cursor()

    # update_statement = cur.prep(config.data_update_req_usd_rate)
    update_statement_1 = cur.prep(config.data_update_req_trend_re_ko)

    # data_change = [['test1', 1], ['test2', 2], ['id 5', 5], ['id 6', 6]]
    # data_change_2 = {1: ('test1_1', 'xx'), 2: ('test2_2', 'yy'), 5: ('id 5_1', 'zz'), 6: ('id 6_1', 'qq')}

    cur.execute(config.data_get_req_1)
    # print(cur)

    updated_data = {}

    for line in cur.fetchall():
        print(line)
        for key, data in data_update.items():
            # if key == line[1]:
            # if key == line[2] and line[1] not in ('1', '2', '3'):
            if key == line[2]:
                # cur.execute(update_statement, (data, key))
                updated_data[line[0]] = data

    # print(updated_data)

    for key, data in updated_data.items():
        cur.execute(update_statement_1, (data, key))

    c.commit()
    c.close()
    print(f'conditional data pump completed, execution time: {round(time.time() - start_time, 0)} seconds')

