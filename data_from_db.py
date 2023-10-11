from connection import db_connect
import config


def from_db_to_data(db: str, request: str, *params):
    c = db_connect(db)
    cur = c.cursor()
    cur.execute(request, (params))
    data_from_db= {}
    for line in cur.fetchall():
        data_from_db[line[0]] = line[1:]
    c.commit()
    c.close()
    return data_from_db


if __name__ == "__main__":
    db_code = input('Data base code: ')
    db = config.db_addresses[db_code]
    num_data_get_req = int(input("Enter data get request number: "))
    req = config.data_get_reqs[num_data_get_req]
    print(from_db_to_data(db, req))
