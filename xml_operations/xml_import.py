import xml.etree.ElementTree as ET
from pathlib import Path

# filepath = input("filepath:")

# filename = input("filename:")

# filename = Path(filepath).joinpath(filename)

filename = 'T:\\YandexDisk\\Wrk\\ЛУКОЙЛ\\НПЗ\\2024\\оценка\\индексы\\rates\\euro\\usd.xml'
result_file = 'T:\\YandexDisk\\Wrk\\ЛУКОЙЛ\\НПЗ\\2024\\оценка\\индексы\\rates\\euro\\euro_rates.csv'

tree = ET.ElementTree(file=filename)

with open(result_file, 'w') as data_f:
    for event, element in ET.iterparse(filename):
        for key, value in element.items():
            print(value)
            data_f.write(f'{value};')
        data_f.write('\n')
