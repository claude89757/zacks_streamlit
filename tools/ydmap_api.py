#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/28 13:25
@Author  : claudexie
@File    : ydmap_api.py
@Software: PyCharm
"""
import requests
import math
import hashlib
import csv
import time
import os
import json
import random
import datetime

# 读取指定环境变量的值
SIGN_KEY = os.environ.get("SIGN_KEY")


def save_to_csv(data_list, filename='data.csv'):
    """
    将数据保存到 CSV 文件
    :param data_list: 数据列表
    :param filename: 文件名
    """
    keys = data_list[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)


def read_from_csv(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = [row for row in reader]
    return data_list


def read_from_csv_by_selected_fields(filename, selected_fields):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = [{field: row[field] for field in selected_fields} for row in reader]
    return data_list


def save_to_json(data_list, json_filename):
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)


def gen_nonce(timestamp: int):
    """
    生成 nonce, 该方法解析自前端 js 代码, 大概率不会变化
    """
    e = int(timestamp)
    y = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    nonce = ''
    for c in y:
        n = math.trunc((e + 16 * random.random()) % 16)
        e = math.floor(e / 16)
        if 'x' == c:
            nonce += hex(n)[2]
        elif 'y' == c:
            nonce += hex(3 & n | 8)[2]
        else:
            nonce += c
    return nonce


def signature_for_post(timestamp: str, nonce: str, param: str = '', data: dict = None):
    """
    生成post请求的签名
    """
    prefix = '&'.join(
        [f'_key={SIGN_KEY}', '_timestamp=' + timestamp, '_nonce=' + nonce])
    prefix += ',,' + param + ',,'
    if data is not None:
        raw = prefix + json.dumps(data, separators=(',', ':'))
    else:
        raw = prefix
    return hashlib.md5(raw.encode()).hexdigest().upper()


def signature_for_get(timestamp: str, nonce: str, param_str: str = ''):
    """
    生成get请求的签名
    """
    prefix = ','.join([
         f'_key={SIGN_KEY}&_timestamp={timestamp}&_nonce={nonce}',
         param_str,
         "",
         "",
         ""
    ])
    print(prefix)
    return hashlib.md5(prefix.encode()).hexdigest().upper()


def clock_to_timestamp(hour: str):
    """
    福田体育的时间戳比较特殊 (奇葩), 它其实是以 2013-01-01 {hour}:00 为基准, 计算出新的时间戳
    其中 hour 为预订时间
    """
    return int(
        datetime.datetime.strptime(f'2013-01-01 {hour}:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)


def timestamp_to_clock(timestamp: int) -> str:
    """
    timestamp 为 Unix 时间戳（毫秒）
    返回值为时钟格式（小时:分钟）
    """
    date = datetime.datetime.fromtimestamp(timestamp / 1000)  # 将毫秒转换为秒
    return date.strftime('%H:%M')


def str_to_timestamp(date_str: str):
    return int(datetime.datetime.strptime(date_str, '%Y-%m-%d').timestamp() * 1000)


def generate_param_str(params):
    # 生成参数字符串
    sorted_keys = sorted(params.keys())
    param_str = "&".join(f"{key}={params[key]}" for key in sorted_keys)
    return param_str


def get_sales_list_by_page(page: int, limit: int) -> dict:
    """
    获取销售列表
    """
    timestamp = math.trunc(time.time() * 1000)
    nonce = gen_nonce(timestamp)
    params = {
        "professional": "200001",
        # "amapLocation": "113.95130947954614,22.528244270998332",
        "searchType": "2",
        "sortType": "2",
        "industryTypes": "1",
        "mapIds": "107292,105110,105218,105213",
        "pageNumber": str(page),
        "pageSize": str(limit),
        "t": str(timestamp)
    }
    param_str = generate_param_str(params)
    signature = signature_for_get(str(timestamp), nonce.replace('-', ''), param_str=param_str)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "entry-tag": "",
        "nonce": nonce.replace('-', ''),
        "openid-token": "",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "signature": signature,
        "timestamp": str(timestamp),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    url = "https://wxsports.ydmap.cn/srv100140/api/pub/sales/getSalesListByPage"

    # 打印调试信息
    print(f"Request URL: {url}")
    print(f"Request Params: {params}")
    print(f"Request Headers: {headers}")

    response = requests.get(url, headers=headers, params=params, timeout=5)

    # 打印响应状态码和内容
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.text))


def get_all_sales_list(limit: int = 50) -> list:
    """
    获取全量销售列表
    example:
            {
          'amapLocation': '114.04629516601562,22.545120239257812',
          'bookingType': 0,
          'commonSalesTels': [{
            'salesExtTel': '',
            'salesTel': '0755-82770388'
          }],
          'distance': 0,
          'district': 442002,
          'id': 101335,
          'imageUrl': 'https://cdn.ydmap.cn/image/36914c23-2631-4fbc-9bcf-4c525742c4ed.jpg',
          'isFavorite': False,
          'isRecommend': False,
          'memo': '',
          'promotionTag': [1],
          'salesAddress': '景田东路和景田南四街交界处（华强职业技术学校西侧）',
          'salesItems': [200001, 200013],
          'salesName': '莲花体育中心',
          'salesSource': 0,
          'salesSubtitle': None,
          'salesTel': '0755-82770388',
          'salesType': 1,
          'subDistrict': 822010,
          'tagTypes': [4]
        }
    """
    all_data = []
    page = 1

    while True:
        response_data = get_sales_list_by_page(page, limit)
        sales_list = response_data.get('data', {}).get('pageRecords', [])
        if not sales_list:
            break
        all_data.extend(sales_list)
        page += 1
        time.sleep(random.uniform(0, 3))
    return all_data


def fetch_hometown_data():
    """
    获取地区ID
    :return:
    """
    url = 'https://cdn.ydmap.cn/json/homeTown.js?t=1724838895931'
    headers = {
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'Referer': 'https://wxsports.ydmap.cn/_/isz/venue.html',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.get(url, headers=headers)
    # 检查响应状态码
    if response.status_code == 200:
        # 获取响应文本
        js_text = response.text.strip("window.$HomeTownArr=")
        # 将 JSON 字符串转换为 Python 列表
        data_list = json.loads(js_text)
        hometown_infos = {}
        for data in data_list:
            hometown_infos[str(data['id'])] = data['name']
        return hometown_infos
    else:
        response.raise_for_status()


# Test
if __name__ == '__main__':
    # sales_list = get_all_sales_list(50)
    # print(f"sales_list: {len(sales_list)}")
    # for court in sales_list:
    #     print(court)
    # data_list = DataCollector(headless=True).run(sales_list)
    # for data in data_list[:10]:
    #     print(data)

    data_list = read_from_csv("tennis_courts_data.csv")

    hometown_infos = fetch_hometown_data()
    # 替换部分数据
    new_data_list = []
    for data in data_list:
        data['district_name'] = hometown_infos.get(data['district'])
        data['sub_district_name'] = hometown_infos.get(data['subDistrict'])
        if data['bookingType'] == '5':
            data['bookingType'] = '电话预约'
        elif data['bookingType'] == '6':
            data['bookingType'] = '暂未开放'
        elif data['bookingType'] == '0':
            data['bookingType'] = 'I深圳APP预约'
        else:
            data['bookingType'] = '其他方式'

        data['bookingLink'] = f"https://wxsports.ydmap.cn/venue/{data['id']}"

        # 特殊说明
        if data['salesName'] == "深圳湾体育中心":
            data['bookingType'] = '非会员当日电话预定，会员支持提前2天预定'
        elif data['salesName'] == "香蜜体育":
            data['bookingType'] = "I深圳APP预约；6号场仅支持当日电话预定"
        else:
            pass
        new_data_list.append(data)

    # 保存数据到 CSV 文件
    save_to_csv(new_data_list, 'new_tennis_courts_data.csv')

    # 从 CSV 文件中读取数据并选取部分字段
    selected_fields = ['district_name',
                       'sub_district_name',
                       'salesName',
                       'bookingLink',
                       'bookingType',
                       'salesTel',
                       'time_range',
                       # 'id',
                       # 'memo',
                       'salesAddress',
                       'court_intro',
                       'other_info']
    data_list = read_from_csv_by_selected_fields('new_tennis_courts_data.csv', selected_fields)

    # 将选取的字段转换为 JSON 并保存到文件
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    save_to_json(data_list, f'tennis_courts_data_{current_date}.json')

    # 保存数据到 CSV 文件
    save_to_csv(data_list, 'show_tennis_courts_data.csv')
