import time
import config
from connection import db_connect


def cond_update(data_update, db: str) -> None:
    try:
        start_time = time.time()

        c = db_connect(db)
        cur = c.cursor()

        num_data_get = int(input("Enter data get type: "))
        num_update = int(input("Enter update type: 1 for average rate, 2 for RE trends, 3 for ME trends, "
                               "4 for ME USD trends: "))
        update_statement_1 = cur.prep(config.data_update_reqs[num_update])
        cur.execute(config.data_get_reqs[num_data_get]) # Base data request should not be changed in most cases

        updated_data = {}

        for line in cur.fetchall():
            if num_update in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
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
            elif num_update in (11, 12, 14):
                for line_u in data_update:
                    if line[1] == line_u[0] and line[2] == line_u[3]: # here may change line_u index. first place -- main data
                        updated_data[line[0]] = line_u[1]
            elif num_update == 13:
                for line_u in data_update:
                    if int(line[0]) == int(line_u[0]): # when compare IDs imported from xlsx they became strings so need to convert to compare with db result set. Spent some time trying to figure out why the function not woking before realizing that
                        updated_data[line[0]] = (line_u[1], line_u[2], line_u[3],)

        for key, data in updated_data.items():
            if num_update != 13:
                cur.execute(update_statement_1, (data, key))
            elif num_update == 13:
                cur.execute(update_statement_1, (data[0], data[1], data[2], key))

        c.commit()
        c.close()
        print(f'Conditional data pump completed, request performed: {config.data_update_reqs[num_update]}','\n',
                f'Execution time: {round(time.time() - start_time, 0)} seconds')
    except Exception as e:
        print(f'Some error occurred: {e}')

    finally:
        c.close()
    # TODO: add requests and source files logging


def cond_update_from_db(db: str) -> None: # to update main_tab with items excluded because of FSBU6
    try:
        start_time = time.time()

        c = db_connect(db)
        cur = c.cursor()

        num_data_get = int(input("Enter data get type: ")) # 2

        num_update = int(input("Enter update type: 1 for average rate, 2 for RE trends, 3 for ME trends, "
                               "4 for ME USD trends: ")) # 10

        div_name = input('Enter plant code: ')

        update_statement_1 = cur.prep(config.data_update_reqs[num_update])

        cur.execute(config.data_get_reqs[num_data_get], (div_name, ))
        # print(cur)

        data_for_update = {}
        for line in cur.fetchall():
            data_for_update[line[0]] = line[1:]

        print('Data from c1_MT downloaded')

        for key, data in data_for_update.items():
            cur.execute(update_statement_1, (data[1], data[2], data[3],
                                             data[4], data[5], data[6], data[7], data [8], data[9], data[10],
                                             data[11], data[12], data[13], data[14], data[15], data[16],
                                             data[17], data[18], key, div_name, )) # need to keep in mind that [0] position of source data set is moved to key, so it becomes one position shorter

        c.commit()
        c.close()
        print(f'Conditional data pump completed, request performed: {config.data_update_reqs[num_update]}', '\n',
                f'Execution time: {round(time.time() - start_time, 0)} seconds')
    except Exception as e:
        print(f'Some error occurred: {e}')

    finally:
        c.close()

# TODO logging: file names and requests used
