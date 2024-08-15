#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/11 14:18
@Author  : claude
@File    : Zacks.py
@Software: PyCharm
"""
import time
import os

import streamlit as st
from sidebar import sidebar

from common.log_config import setup_logger
from common.settings import common_settings_init
from common.tennis_court_data_helper import get_realtime_tennis_court_data


# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="Zacks", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Render Streamlit pages
st.title("深圳热门网球场实时动态")

# Get realtime tennis court data
data_df = get_realtime_tennis_court_data()
