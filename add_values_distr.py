from data_from_db import from_db_to_data
import config
import datetime

db_code = input('Enter data base code: ')  # db code: av_9, req number 8
db = config.db_addresses[db_code]
num_data_get_req = int(input("Enter data get request number: "))  # req number 8 for RE, 9 for ME
req = config.data_get_reqs[num_data_get_req]
kva_div = input('Enter div name: ')  # distribution should be done separately for each company, otherwise collisions due to non-unique invs may occur
data = from_db_to_data(db, req, kva_div)

res = {}
for db_id, asset in data.items(): # 1. определить базовый инв. до /. 2. для всех ОС с таким инв и ненулевым CRN просуммировать CRN и GBV. Дальше как сделано
    if '/' not in asset[0] and asset[1] is not None and asset[2] is not None and asset[1] > 0:
        base_inv = asset[0]
        sum_crn = asset[2]
        sum_gbv = asset[1]
        parts_counts = 1
        base_nl = asset[3]
        if asset[4] is not None and asset[4] > 0:
            base_ea = asset[4]
        else:
            base_ea = ''
        for db_id_2, asset_2 in data.items():
            if base_inv in asset_2[0] and '/' in asset_2[0] and asset_2[1] is not None:
                sum_gbv += asset_2[1]
                parts_counts += 1
        for db_id_3, asset_3 in data.items():
            if base_inv in asset_3[0] and '/' in asset_3[0] and asset_3[2] is not None and asset_3[1] > 0:
                sum_crn += asset_3[2]
        for db_id_4, asset_4 in data.items():
            if base_inv in asset_4[0] and parts_counts > 1 and asset_4[1] > 0:
                # res[db_id_4] = asset_4[1] / sum_gbv * sum_crn
                # res[db_id_4] = base_nl
                res[db_id_4] = (asset_4[1] / sum_gbv * sum_crn, base_nl, base_ea)
            elif base_inv in asset_4[0] and parts_counts > 1 and asset_4[1] == 0:
                res[db_id_4] = (asset_4[2], base_nl, base_ea)
            elif base_inv in asset_4[0] and parts_counts == 1:
                res[db_id_4] = (sum_crn, base_nl, base_ea)

file_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

res_file_name = '6089 kva distr'

with open (f'{res_file_name}_{kva_div}_{num_data_get_req}_{db_code}_{file_time}.csv', 'w') as res_file:
    res_file.write('ID;CRN;N_L;EFF_AGE\n')
    for key, value in res.items():
        res_file.write(str(key) + ';' + ';'.join(map(str, value)) + '\n')
