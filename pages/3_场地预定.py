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
url = "https://wxsports.ydmap.cn/venue/"

st.markdown(f"[点击这里访问场地预定页面]({url})", unsafe_allow_html=True)