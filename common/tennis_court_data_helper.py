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

    # Prepare the time slots from 07:00 to 22:00
    time_slots = [f"{hour:02d}:00" for hour in range(7, 23)]

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
                            if court_name not in table_data[start_time][date]:
                                table_data[start_time][date] += f"{court_name} ({court}), "
                            else:
                                table_data[start_time][date] += f"{court}, "

    # Remove trailing commas and deduplicate court names
    for time_slot in table_data:
        for date in table_data[time_slot]:
            if table_data[time_slot][date]:
                courts = table_data[time_slot][date].split(', ')
                unique_courts = {}
                for court in courts:
                    if court:
                        if ' (' in court:
                            name, number = court.split(' (')
                            number = number.rstrip(')').replace('号场', '')
                        else:
                            name = court
                            number = ''
                        if name not in unique_courts:
                            unique_courts[name] = []
                        if number:
                            unique_courts[name].append(number)
                table_data[time_slot][date] = '\n'.join([f"{name} {len(numbers)}" if numbers else name for name, numbers in unique_courts.items()])

    # Convert the dictionary to a DataFrame for better formatting
    df = pd.DataFrame(table_data).T

    # Apply styles to the DataFrame
    def highlight_cells(val):
        if val:
            return 'background-color: lightblue; color: black'
        return ''

    styled_df = df.style.applymap(highlight_cells).set_properties(**{'white-space': 'pre-wrap'})

    # Display the DataFrame using Streamlit
    st.markdown(
        """
        <style>
        .dataframe tbody tr th, .dataframe tbody tr td {
            white-space: pre-wrap;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(styled_df, height=None, width=800)  # Adjust the width as needed

    return df