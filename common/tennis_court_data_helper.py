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
                                table_data[start_time][date] += f"{court_name}:{court_index}|"
                            else:
                                table_data[start_time][date] += f"|{court_index}"

    # Remove trailing commas and deduplicate court names
    for time_slot in table_data:
        for date in table_data[time_slot]:
            if table_data[time_slot][date]:
                court_name = table_data[time_slot][date].split(':')[0]
                court_index_list = table_data[time_slot][date].split(':')[-1].split('|')
                unique_courts = {}
                for court_index in court_index_list:
                    if unique_courts.get(court_name):
                        unique_courts[court_name].append(court_index)
                    else:
                        unique_courts[court_name] = [court_index]

                # Process the unique_courts dictionary to format the output
                formatted_courts = []
                for name, numbers in unique_courts.items():
                    if "号" in numbers[0]:
                        # If we have specific court numbers, list them
                        court_index_list = []
                        for number in numbers:
                            court_index_list.append(number.split('号')[0])
                        formatted_courts.append(f"{name} ({', '.join(court_index_list)})")
                    else:
                        # If we don't have specific court numbers, just show the count
                        formatted_courts.append(f"{name} {len(numbers)}")
                table_data[time_slot][date] = '\n'.join(formatted_courts)

    # Convert the dictionary to a DataFrame for better formatting
    df = pd.DataFrame(table_data).T
    return df
