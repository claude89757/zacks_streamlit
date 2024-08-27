#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/27 21:47
@Author  : claudexie
@File    : 3_场地预定.py
@Software: PyCharm
"""

import streamlit as st
import os
import json
from io import BytesIO
from PIL import Image
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar
import streamlit.components.v1 as components


# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="场地预定", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# 嵌入外部网页
st.title("场地预定")
url = "https://wxsports.ydmap.cn/venue/"

# 使用 st.components.v1.iframe 嵌入网页
components.iframe(url, width=1200, height=800, scrolling=True)

# 或者使用自定义 HTML 和 CSS 实现自适应 iframe
html_code = f"""
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe src="{url}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
