#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/15 01:06
@Author  : claudexie
@File    : tennis_court_data_helper.py
@Software: PyCharm
"""

import requests
import json
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def format_data_for_markdown(data):
    # Extract dates and time slots
    dates = sorted({date for item in data for date in json.loads(item['content']).keys()})
    time_slots = [f"{hour:02}:00" for hour in range(21, 24)] + [f"{hour:02}:00" for hour in range(0, 8)]

    # Create a DataFrame
    df = pd.DataFrame(index=time_slots, columns=dates)

    for item in data:
        filename = item['filename']
        court_name = filename.split('/')[-1].split('_')[0]  # Extract court name from filename
        content = json.loads(item['content'])

        for date, courts in content.items():
            for court_id, slots in courts.items():
                for start, end in slots:
                    start_hour = int(start.split(':')[0])
                    end_hour = int(end.split(':')[0])
                    if start_hour > 20:  # Evening hours
                        time_slot = f"{start_hour:02}:00"
                        if time_slot in df.index:
                            df.at[time_slot, date] = df.at[time_slot, date] + f"{court_name}, " if pd.notna(
                                df.at[time_slot, date]) else f"{court_name}, "
                    else:  # Early morning hours
                        time_slot = f"{start_hour:02}:00"
                        if time_slot in df.index:
                            df.at[time_slot, date] = df.at[time_slot, date] + f"{court_name}, " if pd.notna(
                                df.at[time_slot, date]) else f"{court_name}, "

    # Clean up the DataFrame
    df = df.fillna('No availability')
    for col in df.columns:
        df[col] = df[col].str.rstrip(', ')

    return df.to_markdown()


def get_realtime_tennis_court_data():
    """
    获取网球场动态数据
    :return:
    """
    data = []
    try:
        # 发送GET请求到API端点
        api_url = F"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON响应
        data = response.json()

        # 格式化数据为Markdown
        markdown_data = format_data_for_markdown(data)
        st.markdown(markdown_data)

    except requests.exceptions.RequestException as e:
        st.error(f"HTTP请求错误: {e}")
    except json.JSONDecodeError as e:
        st.error(f"JSON解析错误: {e}")






