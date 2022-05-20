import openpyxl as opx
import config
from pathlib import Path


class XlsxImport:
    pass


open_path = input('Enter path to file:')
"""File should be in xlsx format"""
file_to_process = input('Enter filename:')
full_data_path = Path(open_path).joinpath(file_to_process)


def get_xlsx_data(data_path=full_data_path, data_workbook_num=config.wb_num):
    wb = opx.load_workbook(data_path)
    sheet = wb.worksheets[data_workbook_num]
    print('xlsx data read completed\n')
    return sheet


def make_data_dict(xlsx_sheet, start_col_num=1, nums_number=10):
    data_d = {}
    row_num = xlsx_sheet.max_row
    # col_num = xlsx_sheet.max_column
    for r_num in range(2, row_num+1):
        # print(str(xlsx_sheet.cell(r_num, col_num).value))
        if xlsx_sheet.cell(r_num, start_col_num).value is not None:
            data_d[str(xlsx_sheet.cell(r_num, start_col_num).value)] = str(xlsx_sheet.cell(r_num, start_col_num + 1).value)
    return data_d


if __name__ == "__main__":
    ws = get_xlsx_data(full_data_path)
    data = make_data_dict(ws)
