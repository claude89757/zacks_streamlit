#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/11 18:52
@Author  : claude
@File    : 1_创建订阅.py
@Software: PyCharm
"""
import time
import os

import streamlit as st
from common.config import CONFIG
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="网球场", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Render Streamlit pages
st.title("网球场")

st.markdown("网球场预定方式汇总")
