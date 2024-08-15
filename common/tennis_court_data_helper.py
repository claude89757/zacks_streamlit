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
    response = requests.get(api_url)
    data = response.json()

    # Get today's date
    today = datetime.today()

    # Prepare the date range for the next 7 days
    date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    # Prepare the time slots from 07:00 to 22:00
    time_slots = [f"{hour:02d}:00" for hour in range(7, 22)]

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
                                table_data[start_time][date] += f"|{court_name}:{court_index}"
                            else:
                                table_data[start_time][date] += f",{court_index}"

    # 设置分栏
    cols = st.columns(2)  # 创建两栏布局

    # 计数器，用于在不同的列中展示内容
    counter = 0

    # 显示卡片内容
    for time, schedules in table_data.items():
        with cols[counter % 2]:  # 在两栏中交替显示
            st.markdown(f"### {time}")
            for date, locations in schedules.items():
                st.markdown(f"**{date}**")
                locations = locations.replace('|', ', ')
                st.write(locations)
                st.markdown("---")
        counter += 1

    # 将数据转换为 HTML 表格格式
    html_table = """
    <table border="1" style="width:100%; text-align:center;">
      <thead>
        <tr>
          <th>时间</th>
    """

    # 动态获取日期列标题
    dates = list(next(iter(table_data.values())).keys())
    for date in dates:
        html_table += f"<th style='width:auto;'>{date}</th>"

    html_table += """
        </tr>
      </thead>
      <tbody>
    """

    # 添加每个时间段的数据
    for time, schedules in table_data.items():
        html_table += f"<tr><td style='text-align:left;'>{time}</td>"
        for date in dates:
            locations = schedules.get(date, "")
            if not locations:
                locations = "广告位招租"  # 显示“广告位招租”占位符
            # 使用 <br> 实现自动换行并将内容左对齐
            locations = locations.replace('|', '<br>')
            html_table += f"<td style='width:auto; text-align:left;'>{locations}</td>"
        html_table += "</tr>"

    html_table += """
      </tbody>
    </table>
    """

    # 使用 Streamlit 显示表格
    st.markdown(html_table, unsafe_allow_html=True)



    # # Remove trailing commas and deduplicate court names
    # for time_slot in table_data:
    #     for date in table_data[time_slot]:
    #         if table_data[time_slot][date]:
    #             courts = table_data[time_slot][date].split(', ')
    #             unique_courts = {}
    #             for court in courts:
    #                 if court:
    #                     if ' (' in court:
    #                         name, number = court.split(' (')
    #                         number = number.rstrip(')').replace('号场', '')
    #                     else:
    #                         name = court
    #                         number = ''
    #                     if name not in unique_courts:
    #                         unique_courts[name] = []
    #                     if number:
    #                         unique_courts[name].append(number)
    #             # Process the unique_courts dictionary to format the output
    #             formatted_courts = []
    #             for name, numbers in unique_courts.items():
    #                 if numbers:
    #                     # If we have specific court numbers, list them
    #                     formatted_courts.append(f"{name} ({', '.join(numbers)})")
    #                 else:
    #                     # If we don't have specific court numbers, just show the count
    #                     formatted_courts.append(f"{name} {len(numbers)}")
    #             table_data[time_slot][date] = '\n'.join(formatted_courts)

    # Convert the dictionary to a DataFrame for better formatting
    df = pd.DataFrame(table_data).T
    return df
