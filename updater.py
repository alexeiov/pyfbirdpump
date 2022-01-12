import fdb
import time

import config

startTime = time.time()


def db_connect():
    con = fdb.connect(dsn=config.address, user=config.username, password=config.passwd,
                      charset='win1251')
    return con


c = db_connect()
cur = c.cursor()

update_statement = cur.prep(config.data_update_req)

data_change = [['test1', 1], ['test2', 2], ['id 5', 5], ['id 6', 6]]
data_change_2 = {1: ('test1', 'xx'), 2: ('test2', 'yy'), 5: ('id 5', 'zz'), 6: ('id 6', 'qq')}


for key, data in data_change_2.items():
    cur.execute(update_statement, (data[0], data[1], key))

print(f'data pump completed, execution time: {time.time() - startTime} seconds')
c.commit()
c.close()
