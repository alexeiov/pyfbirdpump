import openpyxl as opx
import config
from pathlib import Path
from connection import db_connect
import datetime

db_name = config.address[-17:-4]
# base_filename = '5856_VSMPO_calculation_example_'
exported_filename = db_name + '_calculation_example_' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.xlsx' #Todo Get DB name from db
save_path = input('Please insert save path: ')
full_save_path = Path(save_path).joinpath(exported_filename)


def get_names(req):
    # procedure_field_names = input('Insert request to db to get field names: ')
    procedure_field_names = req
    proc_names = []
    c = db_connect()
    cur = c.cursor()
    cur.execute(procedure_field_names)
    names = cur.fetchall()
    for name in names:
        if name[0][0:2] != 'IP':
            proc_names.append(name[0].strip())
    return proc_names


def get_data(req):
    # data_get_example = input('Insert request to db to get valuation data: ')
    data_get_example = req
    data = []
    c = db_connect()
    cur = c.cursor()
    cur.execute(data_get_example)
    print('Export is in progress')
    # k = 0
    for line in cur.fetchall():
        # print(line)
        # while k < 200:
        #     print('.', end='')
        data.append(line)
        # k += 1
    # print('\n')
    c.close()
    return data


# def get_coeffs(req):
#     data = []
#     c = db_connect()
#     cur = c.cursor()
#     cur.execute(req)
#     for line in cur.fetchall():
#         data.append(line)
#     return data


def save_results_to_xlsx(save_p, *res_sets): # Todo any number of sheets, first with formulas, other - simple export

    P_CRN_PREV = 'G'
    P_TREND_COEFF = 'N'
    P_IDC_COEFF_PREV = 'J'
    P_DIRECT_COEFF = 'K'
    P_INDIRECT_COEFF = 'L'
    P_DIRECT_COEFF_PREV = 'H'
    P_INDIRECT_COEFF_PREV = 'I'
    P_IDC_COEFF = 'M'
    P_EURO_PREV = 'Q'
    P_EURO_CURRENT = 'S'
    P_USD_PREV = 'P'
    P_USD_CURRENT = 'R'

    CRN_CALC_C_NUM = 21

    wb = opx.Workbook()
    sheet_main_title = 'calculation_example'
    wb.create_sheet(sheet_main_title, 0)
    sheet_coeffs_prev_title = 'crn_trend_coeffs'
    wb.create_sheet(sheet_coeffs_prev_title, 1)

    names_r = res_sets[0]
    names_c = res_sets[1]
    results = res_sets[2]
    coeffs = res_sets[3]

    for n_num, name in enumerate(names_r):
        wb.worksheets[0].cell(1, n_num + 1).value = name

    for r_num, row in enumerate(results):
        for cell_num, cell in enumerate(row):
            wb.worksheets[0].cell(r_num + 2, cell_num + 1).value = cell
            if row[2] in ('0', '1', '2', '3') and row[14][:10] == 'index_prev':
                wb.worksheets[0].cell(r_num + 2, CRN_CALC_C_NUM).value = f'= {P_CRN_PREV}{r_num + 2} / {P_IDC_COEFF_PREV}{r_num + 2} * {P_IDC_COEFF}{r_num + 2} * {P_TREND_COEFF}{r_num + 2}'
            elif row[2] not in ('0', '1', '2', '3', 'CIP') and row[14][:2] == 'ru':
                wb.worksheets[0].cell(r_num + 2, CRN_CALC_C_NUM).value = f'= {P_CRN_PREV}{r_num + 2} / {P_IDC_COEFF_PREV}{r_num + 2} / {P_DIRECT_COEFF_PREV}{r_num + 2} / {P_INDIRECT_COEFF_PREV}{r_num + 2} * {P_IDC_COEFF}{r_num + 2} * {P_TREND_COEFF}{r_num + 2} * {P_INDIRECT_COEFF}{r_num + 2} * {P_DIRECT_COEFF}{r_num + 2}'

    for n_num, name in enumerate(names_c):
        wb.worksheets[1].cell(1, n_num + 1).value = name

    for r_num, row in enumerate(coeffs):
        for cell_num, cell in enumerate(row):
            wb.worksheets[1].cell(r_num + 2, cell_num + 1).value = cell

    wb.save(filename=save_p)
    print('Export completed')


def sv_round(num):
    pass


n_d = get_names("select RDB$parameter_name from rdb$procedure_parameters where rdb$procedure_name = 'CALC_EXAMPLE' order by rdb$parameter_number")
n_c = get_names("select rdb$field_name from rdb$relation_fields where rdb$relation_name = 'TREND_COEFFS' order by RDB$FIELD_POSITION")

d = get_data("select * from calc_example('VSMPO') rows 5000")
c = get_data("select * from TREND_COEFFS")
save_results_to_xlsx(full_save_path, *(n_d, n_c, d, c,))
