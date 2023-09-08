import csv
import datetime
import json

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xmltodict
import config

# browser = webdriver.Firefox(executable_path=r'T:\\YandexDisk\\Wrk\\Общая информация\\Справочная информация\\ИТ в оценке\\pyfbirdpump\\venv\\Scripts\\geckodriver.exe')
# browser.get('https://ovsiannikov.net')
# time.sleep(3)

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
headers = {'User-Agent': user_agent, }


def get_av_rub_rates(curr, start_date, finish_date):
    """
    Функция для импорта ежедневных данных об обменном курсе с сайта ЦБР и расчёта среднемесячных значений
    """
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


def get_us_fred_trends(api_key, ser_id, start_date, end_date):
    """
    Функция для импорта индексов цен производителей промышленного оборудования и промышленных зданий в США
    Документация: https://fred.stlouisfed.org/docs/api/fred/, https://fred.stlouisfed.org/docs/api/fred/category_series.html
    https://fred.stlouisfed.org/docs/api/fred/series.html, https://fred.stlouisfed.org/docs/api/fred/series_observations.html
    """

    # url_s = f"https://api.stlouisfed.org/fred/series?series_id={ser_id}&api_key={api_key}&realtime_start={start_date}&realtime_end={end_date}&file_type=json"
    url_d = f"https://api.stlouisfed.org/fred/series/observations?series_id={ser_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&file_type=json"
    # url = f"https://api.stlouisfed.org/fred/category/series?category_id=125&api_key=={api_key}&realtime_start={start_date}&realtime_end={end_date}&file_type=json"
    r = requests.get(url=url_d, headers=headers)
    return json.loads(r.text)


def get_jap_tools():
    pass


# print(rates[0])
# print(rates)
if __name__ == "__main__":

    curr_cbr_code = 'R01235'
    start_date = '01/01/2010'
    end_date = '01/02/2023'

    download_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    curr_db_code = None

    if curr_cbr_code == 'R01235':
        curr_db_code = 0
    elif curr_cbr_code == 'R01239':
        curr_db_code = 2
    else:
        pass

    rates = get_av_rub_rates(curr_cbr_code, start_date, end_date)
    with open(f'rates_{download_time}_{curr_cbr_code}_{start_date.replace("/", "")}_{end_date.replace("/", "")}.csv', 'w') as rates_file:
        rates_file.write(f'MON_Y;AV_RATE;CURR_ID\n')
        for date, rate in rates.items():
            rates_file.write(f'{date};{rate};{curr_db_code}\n')

    ble_trend_type = 'china_me'  # choose trend type here (see config for details)

    res = get_us_fred_trends(config.fred_api_key, config.fred_series_id[ble_trend_type], "2010-01-01", "2023-02-01")

    with open(f'{ble_trend_type}_trends.csv', 'w', newline='') as tr_f:
        writer = csv.writer(tr_f, delimiter=';')
        writer.writerow(('Date', 'Index'))
        for d in res['observations']:
            print(d['date'], d['value'])
            # tr_f.write(d['date'] + ';' + d['value'])
            writer.writerow((d['date'], d['value']))
