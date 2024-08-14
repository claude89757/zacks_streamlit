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
    api_url = f"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"

    # Fetch data from API
    response = requests.get(api_url)
    data = response.json()

    # Get today's date
    today = datetime.today()

    # Prepare the date range for the next 7 days
    date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    # Prepare the time slots from 21:00 to 07:00 in reverse order
    time_slots = [f"{hour:02d}:00" for hour in range(21, 24)] + [f"{hour:02d}:00" for hour in range(0, 8)]
    time_slots.reverse()

    # Initialize a dictionary to hold the table data
    table_data = {time_slot: {date: '' for date in date_range} for time_slot in time_slots}

    # Process each file's content
    for file in data:
        content = json.loads(file['content'])
        filename = file['filename']
        court_name = filename.replace('/root/', '').replace('_available_court.txt', '')

        for date, courts in content.items():
            if date in date_range:
                for court, slots in courts.items():
                    for slot in slots:
                        start_time, end_time = slot
                        if start_time in table_data and date in table_data[start_time]:
                            table_data[start_time][date] += f"{court_name} ({court}), "

    # Convert the dictionary to a DataFrame for better formatting
    df = pd.DataFrame(table_data).T

    # Print the DataFrame as a table
    print(df.to_string())
    return df
