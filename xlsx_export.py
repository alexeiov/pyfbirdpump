import openpyxl as opx
import config
from pathlib import Path
from connection import db_connect
import time


def get_names():
    proc_names = []
    c = db_connect()
    cur = c.cursor()
    cur.execute(config.procedure_field_names)
    names = cur.fetchall()
    for name in names:
        if name[0][0] == 'P':
            proc_names.append(name[0].strip())
    return proc_names


def get_data():
    data = []
    c = db_connect()
    cur = c.cursor()
    cur.execute(config.data_get_example)
    for line in cur.fetchall():
        print(line)
        data.append(line)
    return data


def save_results_to_xlsx(results, names, save_path):
    wb = opx.Workbook()
    sheet = wb.worksheets[0]
    sheet.title = 'calculation_example'

    for n_num, name in enumerate(names):
        sheet.cell(1, n_num + 1).value = name

    for r_num, row in enumerate(results):
        for cell_num, cell in enumerate(row):
            sheet.cell(r_num + 2, cell_num + 1).value = cell

    wb.save(filename=save_path)


n = get_names()
d = get_data()
save_results_to_xlsx(d, n, "test_example.xlsx")
