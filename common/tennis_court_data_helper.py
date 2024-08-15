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
import streamlit as st


def set_realtime_tennis_court_sheet():
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
    current_min = today.strftime('%H:%M')

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
                                table_data[start_time][date] += f"|{court_name}:{0}"
                            else:
                                table_data[start_time][date] += f",{0}"
                            table_data[start_time][date] = table_data[start_time][date].strip("|")

    # 将数据转换为 HTML 表格格式
    html_table = F"""
        <table border="1" style="width:100%; text-align:center; table-layout: auto;">
          <thead>
            <tr>
              <th style="background-color: white; white-space: nowrap;">{current_min}<br>🎾</th>
    """

    # 动态获取日期列标题和星期名称
    for weekday, date in zip(weekdays, date_range):
        weekday_cn = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四',
                      'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'}[weekday]
        if weekday_cn in ["星期六", "星期日"]:
            html_table += f"<th style='background-color: #00BFFF; width:auto; white-space: nowrap;'>{weekday_cn}<br>{date[5:]}</th>"
        else:
            html_table += f"<th style='background-color: #7DF9FF; width:auto; white-space: nowrap;'>{weekday_cn}<br>{date[5:]}</th>"

    html_table += """
            </tr>
          </thead>
          <tbody>
    """

    # 添加每个时间段的数据
    for i, time in enumerate(time_slots):
        # 判断是否为过去或当前小时
        schedules = table_data[time]
        # 第一列的第二行开始的时间用淡蓝色填充
        time_cell_style = "background-color: #fcfbf7;" if i >= 4 else "background-color: #fcefed;"
        html_table += f"<tr><td style='{time_cell_style} text-align:left; white-space: nowrap;'>{time}</td>"
        for date in date_range:
            cell_background_color = "#f5f5f5" if (time <= current_hour and today_str in date) else "white"
            locations = schedules.get(date, "")
            if not locations:
                locations = ""  # 显示“广告位招租”占位符
                cell_background_color = "#f5f5f5"
            # 使用 <br> 实现自动换行并将内容左对齐
            locations = locations.replace('|', '<br>')
            html_table += f"<td style='background-color: {cell_background_color}; width:auto; text-align:left; white-space: nowrap;'>{locations}</td>"
        html_table += "</tr>"

    html_table += """
          </tbody>
        </table>
    """

    # 使用 Streamlit 显示表格
    st.markdown(html_table, unsafe_allow_html=True)
