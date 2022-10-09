import xml.etree.ElementTree as ET
import config
from pathlib import Path
import os
import datetime
from connection import db_connect
from file_path_getter import get_path

# full_data_path = get_path()
db = config.db_addresses['kva_6']


def get_data_from_db(req):
    data_get_example = req
    data = []
    c = db_connect(db)
    cur = c.cursor()
    cur.execute(data_get_example)
    print('Export is in progress')

    for line in cur.fetchall():
        data.append(line)
    c.close()
    print('Export finished')
    return data


def make_xml(data, file_name):
    root = ET.Element('kva_20220630_fa_valuation')
    root.set('xlmns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    # xlmns = ET.Element("http://www.w3.org/2001/XMLSchema-instance")
    # root.append(xlmns)
    for row_num in range(len(data)):
        row = ET.Element('row')
        root.append(row)
        # append ID
        r0 = ET.SubElement(row, 'id')
        r0.text = str(data[row_num][0])

        # append aar_gr
        r1 = ET.SubElement(row, 'aar_gr')
        r1.text = str(data[row_num][1])

        # append msfo_class
        r2 = ET.SubElement(row, 'msfo_class')
        r2.text = data[row_num][2]

        # append div
        r3 = ET.SubElement(row, 'div')
        r3.text = data[row_num][3]

        # append valuation currency
        r4 = ET.SubElement(row, 'valuation_currecny')
        r4.text = data[row_num][4]

        # append rate rub
        r5 = ET.SubElement(row, 'rate_rub')
        r5.text = str(data[row_num][5])

        # append inv number
        r6 = ET.SubElement(row, 'inv')
        r6.text = data[row_num][6]

        # append name
        r7 = ET.SubElement(row, 'name')
        r7.text = data[row_num][7]

        # append date_in
        r8 = ET.SubElement(row, 'date_in')
        r8.text = str(data[row_num][8])

        # append CRN_VC
        r9 = ET.SubElement(row, 'CRN_VC')
        r9.text = str(data[row_num][9])

        # append CRN_USD
        r10 = ET.SubElement(row, 'CRN_USD')
        r10.text = str(data[row_num][10])

        # append CRN_RUB
        r11 = ET.SubElement(row, 'CRN_RUB')
        r11.text = str(data[row_num][11])

        # append CORLP_VC
        r12 = ET.SubElement(row, 'CORLP_VC')
        r12.text = str(data[row_num][12])

        # append CORLP_USD
        r13 = ET.SubElement(row, 'CORLP_USD')
        r13.text = str(data[row_num][13])

        # append CORLP_RUB
        r14 = ET.SubElement(row, 'CORLP_RUB')
        r14.text = str(data[row_num][14])

        # append CORLD_VC
        r15 = ET.SubElement(row, 'CORLD_VC')
        r15.text = str(data[row_num][15])

        # append CORLD_USD
        r16 = ET.SubElement(row, 'CORLD_USD')
        r16.text = str(data[row_num][16])

        # append CORLD_RUB
        r17 = ET.SubElement(row, 'CORLD_RUB')
        r17.text = str(data[row_num][17])

        # append FMV_VC
        r18 = ET.SubElement(row, 'FMV_VC')
        r18.text = str(data[row_num][18])

        # append FMV_USD
        r19 = ET.SubElement(row, 'FMV_USD')
        r19.text = str(data[row_num][19])

        # append FMV_RUB
        r20 = ET.SubElement(row, 'FMV_RUB')
        r20.text = str(data[row_num][20])

        # append N_L
        r21 = ET.SubElement(row, 'N_L')
        r21.text = str(data[row_num][21])

        # append R_LIFE
        r22 = ET.SubElement(row, 'R_LIFE')
        r22.text = str(data[row_num][22])

        # append GBV_N
        r23 = ET.SubElement(row, 'GBV_N')
        r23.text = str(data[row_num][23])

        # append NBV_N
        r24 = ET.SubElement(row, 'NBV_N')
        r24.text = str(data[row_num][24])

        # append VALUATION_TYPE
        r25 = ET.SubElement(row, 'VALUATION_TYPE')
        r25.text = str(data[row_num][25])

        # append CAP_INT_END
        r26 = ET.SubElement(row, 'CAP_INT_END')
        r26.text = str(data[row_num][26])

        # append LIQ_VALUE
        r27 = ET.SubElement(row, 'LIQ_VALUE')
        r27.text = str(data[row_num][27])

    tree = ET.ElementTree(root)

    with open(file_name, 'wb') as xml_file:
        tree.write(xml_file)


if __name__ == "__main__":
    file_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = f'5923_kva_fa_valuation_20220630_{file_time}.xml'
    req = config.data_get_reqs[7]
    data = get_data_from_db(req)
    make_xml(data, file_name)
