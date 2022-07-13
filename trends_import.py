import csv

import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import xmltodict

# browser = webdriver.Firefox(executable_path=r'T:\\YandexDisk\\Wrk\\Общая информация\\Справочная информация\\ИТ в оценке\\pyfbirdpump\\venv\\Scripts\\geckodriver.exe')
# browser.get('https://ovsiannikov.net')
# time.sleep(3)

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
headers = {'User-Agent': user_agent, }

"""
Функция для импорта ежедневных данных об обменном курсе с сайта ЦБР
"""
def get_av_rub_rates(curr, start_date, finish_date):
    url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={finish_date}&VAL_NM_RQ={curr}"
    r = requests.get(url=url, headers=headers)
    rates = xmltodict.parse(r.text)['ValCurs']['Record']
    rates_l = [([int(d) for d in rate['@Date'].split('.')], float(rate['Value'].replace(',', '.'))) for rate in rates]

    # with open('rates_test.csv', 'w', newline= '') as rates_f: # Сохранение файла с курсами для проверки расчёта среднего
    #     writer = csv.writer(rates_f, delimiter = ';')
    #     for rate in rates:
    #         writer.writerow((rate['@Date'], rate['Value']))
        # rates_f.write(rate['@Date'] + ';' + rate['Value'])

    av_rates = {}
    for rate in rates_l:
        if str(rate[0][1]) + '_' + str(rate[0][2]) in av_rates:
            pass
        else:
            av_rates[str(rate[0][1]) + '_' + str(rate[0][2])] = ''
    for mon_y in av_rates.keys():
        counts = 0
        summ = 0
        for rate in rates_l:
            if str(rate[0][1]) + '_' + str(rate[0][2]) == mon_y:
                summ += rate[1]
                counts += 1
        av_rates[mon_y] = summ / counts
    return av_rates


def get_rus_me_trends():
    pass


def get_rus_re_trends():
    pass


def get_eurostat_me():
    pass


def get_ble_trends():
    pass


def get_jap_tools():
    pass


rates = get_av_rub_rates('R01235', '01/01/2022', '31/05/2022')
# print(rates[0])
print(rates)
