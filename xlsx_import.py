import openpyxl as opx
import config

inputData = []
wb = opx.load_workbook(filename=config.datasource)
sheet = wb.worksheets[0]

print('xlsx data read completed\n')