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
from common.config import CONFIG
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="Zacks", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Render Streamlit pages
st.title("Zacks")

st.markdown("This is new Zacks Web!")
