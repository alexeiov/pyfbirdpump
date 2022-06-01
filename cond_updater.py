import time
import config
from connection import db_connect


def cond_update(data_update: dict, db: str) -> None:
    try:
        start_time = time.time()

        c = db_connect(db)
        cur = c.cursor()

        num_update = int(input("Enter update type: 1 for average rate, 2 for RE trends, 3 for ME trends, "
                               "4 for ME USD trends: "))

        update_statement_1 = cur.prep(config.data_update_reqs[num_update])

        cur.execute(config.data_get_req_1) # Base data request should not be changed in most cases
        # print(cur)

        updated_data = {}

        for line in cur.fetchall():
            for key, data in data_update.items(): # Standart structure of the data for conditional upload to table: two columns, 1st - key, 2nd - data
                # if key == line[1]:
                if num_update in (3, 4, 9):
                    if key == line[3] and line[1] not in ('0', '1', '2', '3', 'CIP'):
                    # if key == line[3]:
                        # cur.execute(update_statement_1, (data, key))
                        updated_data[line[0]] = data
                elif num_update in (1, 2, 5, 6, 7, 8):
                    if key == line[3]:
                        updated_data[line[0]] = data

        for key, data in updated_data.items():
            cur.execute(update_statement_1, (data, key))

        c.commit()
        c.close()
        print(f'Conditional data pump completed, request performed: {config.data_update_reqs[num_update]}', '\n',
                f'Execution time: {round(time.time() - start_time, 0)} seconds')
    except Exception as e:
        print(f'Some error occurred: {e}')

    finally:
        c.close()
    # TODO: add requests and source files logging
