#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/13 22:37
@Author  : claude
@File    : sidebar.py
@Software: PyCharm
"""
import streamlit as st
import json
import os
from datetime import datetime

# Define the path to the local file where we will store the data
DATA_FILE = "app_data.json"

# Initialize the data structure
if not os.path.exists(DATA_FILE):
    data = {
        "total_visits": 0,
        "monthly_visits": {},
        "daily_visits": {},
        "users": []
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
else:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

# Get the current date and month
current_date = datetime.now().strftime("%Y-%m-%d")
current_month = datetime.now().strftime("%Y-%m")

# Update the visit counts
data["total_visits"] += 1
data["daily_visits"][current_date] = data["daily_visits"].get(current_date, 0) + 1
data["monthly_visits"][current_month] = data["monthly_visits"].get(current_month, 0) + 1

# Update the user count
if "phone_number" in st.session_state:
    data["users"].append(st.session_state["phone_number"])

# Save the updated data back to the file
data["users"] = list(data["users"])  # Convert set to list for JSON serialization
with open(DATA_FILE, "w") as f:
    json.dump(data, f)


# Sidebar component to display the statistics
def sidebar():
    st.sidebar.subheader("App Statistics")

    # Create columns for a more compact layout
    col1, col2 = st.sidebar.columns(2)

    # Display today's visits
    col1.metric("Today's Visits", data['daily_visits'].get(current_date, 0))

    # Display monthly visits
    col2.metric("Monthly Visits", data['monthly_visits'].get(current_month, 0))

    # Display total visits
    st.sidebar.metric("Total Visits", data['total_visits'])

    # Display total users
    st.sidebar.metric("Total Users", len(set(data['users'])))

    # Optionally, add a progress bar for monthly visits
    monthly_goal = 1000  # Example goal for monthly visits
    monthly_visits = data['monthly_visits'].get(current_month, 0)
    progress = min(monthly_visits / monthly_goal, 1.0)
    st.sidebar.progress(progress)

    # Add some additional styling or information if needed
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Keep up the good work!**")
    st.sidebar.markdown("Thank you for using our app.")
