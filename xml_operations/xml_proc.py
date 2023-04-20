import csv
import xml.etree.ElementTree as ET
import config
from pathlib import Path
import os
import datetime

xml_source = config.data_file_a
# xml_data_file = 'vsmpo_reg_extr.csv'
xml_data_file = os.path.basename(xml_source)[:6] +'_' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '_xml_reg_analysis.csv'
save_path = input('Please insert save path: ')
full_save_path = Path(save_path).joinpath(xml_data_file)

tree = ET.parse(xml_source)
root = tree.getroot()
row_counts = 0
reg = []
for i, row in enumerate(root):
    row_counts += 1
    data = {}
    for column in row:
        # print(column.tag)
        if column.tag == 'inv':
            data['inv'] = column.text
        if column.tag == 'name':
            data['name'] = column.text
        if column.tag == 'msfo_class':
            data['msfo_class'] = column.text
        if column.tag == 'gbv':
            data['gbv'] = float(column.text)
        if column.tag == 'nbv':
            data['nbv'] = column.text
            reg.append(data)
            continue

# print(reg)
# print(row_counts)
summary = {}
for row in reg:
    if row['msfo_class'] in summary:
        summary[row['msfo_class']]['asset_counts'] += 1
        summary[row['msfo_class']]['sum_gbv'] += float(row['gbv'])
        summary[row['msfo_class']]['sum_nbv'] += float(row['nbv'])
    else:
        summary[row['msfo_class']] = {'asset_counts': 1, 'sum_gbv': float(row['gbv']), 'sum_nbv': float(row['nbv'])}

print(summary)

# with open (full_save_path, 'w', newline='') as file_reg_extr:
#     for row in reg:
#         file_reg_extr.writelines('\'' + row['inv'] + ';' + row['name'] + ';' + str(row['gbv']) + '\n')

with open (full_save_path, 'w', newline='') as file_reg_extr:
    for group, data in summary.items():
        file_reg_extr.writelines(group + ';' + str(data['asset_counts'])  + ';' + str(data['sum_gbv']) + ';' + str(data['sum_nbv']) + '\n')
