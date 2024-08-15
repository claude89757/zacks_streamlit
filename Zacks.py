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
from common.tennis_court_data_helper import set_realtime_tennis_court_sheet


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
set_realtime_tennis_court_sheet()

# 创建选项卡
tab1, tab2, tab3 = st.tabs(["自定义名称1", "自定义名称2", "自定义名称3"])

with tab1:
    st.write("这是自定义名称1的内容")

with tab2:
    st.write("这是自定义名称2的内容")

with tab3:
    st.write("这是自定义名称3的内容")