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
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


def get_realtime_tennis_court_data():
    """
    查询场地数据
    :return:
    """
    api_url = f"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"

    # Fetch data from API
    response = requests.get(api_url, timeout=10)
    data = response.json()

    # Get today's date and current time
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    current_hour = today.strftime('%H:00')

    # Prepare the date range for the next 7 days and their weekday names
    date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    weekdays = [(today + timedelta(days=i)).strftime('%A') for i in range(7)]

    # Prepare the time slots from 07:00 to 22:00 (倒序)
    time_slots = [f"{hour:02d}:00" for hour in range(21, 6, -1)]

    # Initialize a dictionary to hold the table data
    table_data = {time_slot: {date: '' for date in date_range} for time_slot in time_slots}

    # Process each file's content
    for file in data:
        content = json.loads(file['content'])
        filename = file['filename']
        court_name = filename.replace('/root/', '').replace('_available_court.txt', '')

        for date, courts in content.items():
            if date in date_range:
                for court_index, slots in courts.items():
                    for slot in slots:
                        start_time, end_time = slot
                        if start_time in table_data and date in table_data[start_time]:
                            if court_name not in table_data[start_time][date]:
                                table_data[start_time][date] += f"\n{court_name}:{0}"
                            else:
                                table_data[start_time][date] += f",{0}"

    # 将数据转换为 HTML 表格格式
    html_table = """
        <table border="1" style="width:100%; text-align:center;">
          <thead>
            <tr>
              <th style="background-color: #f2f2f2;">刷新</th>
    """

    # 动态获取日期列标题和星期名称
    for weekday, date in zip(weekdays, date_range):
        html_table += f"<th style='background-color: #f2f2f2; width:auto;'>{weekday}<br>{date[5:]}</th>"

    html_table += """
            </tr>
          </thead>
          <tbody>
    """

    # 添加每个时间段的数据
    for time in time_slots:
        # 判断是否为过去或当前小时

        schedules = table_data[time]
        html_table += f"<tr><td style='background-color: #f2f2f2; text-align:left;'>{time}</td>"
        for date in date_range:
            cell_background_color = "#d3d3d3" if time <= current_hour and today_str in data else "white"
            locations = schedules.get(date, "")
            if not locations:
                locations = "广告位招租"  # 显示“广告位招租”占位符
            # 使用 <br> 实现自动换行并将内容左对齐
            locations = locations.replace('|', '<br>')
            html_table += f"<td style='background-color: {cell_background_color}; width:auto; text-align:left;'>{locations}</td>"
        html_table += "</tr>"

    html_table += """
          </tbody>
        </table>
    """

    # 使用 Streamlit 显示表格
    st.markdown(html_table, unsafe_allow_html=True)
