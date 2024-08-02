import requests
import csv

# 引用 BlockingScheduler 類別
from apscheduler.schedulers.blocking import BlockingScheduler

def get_api_data(API_URL):
    headers = {
     'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    #   發出網路請求
    resp = requests.get(API_URL, headers = headers)

    # 使用 json 方法可以將回傳值從 JSON 格式轉成 Python dict 字典格式方便存取
    data = resp.json()
    return data

def get_parse_data(data):
    Station_records = data['records']['Station']

    # 宣告一個暫存列表 list
    row_list = []

    # 一一取出 r-ent 區塊
    for Station_records in Station_records :
        # 從 JSON 檔案轉成 dict/list 中取值
        lat = Station_records['GeoInfo']['Coordinates'][0]['StationLatitude']
        lon = Station_records['GeoInfo']['Coordinates'][0]['StationLongitude']
        locationName = Station_records['StationName']
        stationId = Station_records['StationId']
        obsTime = Station_records['ObsTime']['DateTime']
        ELE = Station_records['GeoInfo']['StationAltitude']
        WDIR = Station_records['WeatherElement']['WindDirection']
        WDSD = Station_records['WeatherElement']['WindSpeed']
        TEMP = Station_records['WeatherElement']['AirTemperature']
        HUMD = Station_records['WeatherElement']['RelativeHumidity']
        PRES = Station_records['WeatherElement']['AirPressure']
        # 將資料整理成一個 dict
        data = {}
        data['lat'] = lat
        data['lon'] = lon
        data['locationName'] = locationName
        data['stationId'] = stationId
        data['obsTime'] = obsTime
        data['ELE'] = ELE
        data['WDIR'] = WDIR
        data['WDSD'] = WDSD
        data['TEMP'] = TEMP
        data['HUMD'] = HUMD
        data['PRES'] = PRES
        # 存入 row_list 方便之後寫入 csv 檔案使用
        row_list.append(data)

    return row_list

def save_data_to_csv(row_list):
    # CSV 檔案第一列標題記得要和 dict 的 key 相同，不然會出現錯誤
    headers = ['lat', 'lon', 'locationName', 'stationId', 'obsTime', 'ELE', 'WDIR', 'WDSD', 'TEMP', 'HUMD', 'PRES']

    # 使用檔案 with ... open 開啟 write (w) 寫入檔案模式，透過 csv 模組將資料寫入
    with open('weather.csv', 'w') as output_files:
        dict_writer = csv.DictWriter(output_files, headers)
        # 寫入標題
        dict_writer.writeheader()
        # 寫入值
        dict_writer.writerows(row_list)

# 創建一個 Scheduler 物件實例
sched = BlockingScheduler({'apscheduler.timezone' : 'Asia/Taipei'})

# decorator 設定 Scheduler 的類型和參數，例如 interval 間隔多久執行
@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('每 10 秒執行一次程式工作區塊')
    API_URL = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=rdec-key-123-45678-011121314'
    data = get_api_data(API_URL)
    row_list = get_parse_data(data)
    save_data_to_csv(row_list)

sched.start()
