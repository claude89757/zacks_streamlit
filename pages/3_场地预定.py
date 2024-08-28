import time

import streamlit as st
import os
import json
from io import BytesIO
from PIL import Image
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="场地预定", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# 提供外部网页的链接
st.title("场地预定")

# 目标URL
target_url = "https://wxsports.ydmap.cn/venue/"

# 使用HTML和JavaScript实现自动跳转
html_code = f"""
    <meta http-equiv="refresh" content="0; url={target_url}" />
    <script type="text/javascript">
        window.location.href = "{target_url}";
    </script>
    <p>If you are not redirected automatically, follow this <a href="{target_url}">link to the target page</a>.</p>
"""

st.warning("正在跳转至订场页面...")
time.sleep(3)
# 在Streamlit中显示HTML代码
st.markdown(html_code, unsafe_allow_html=True)