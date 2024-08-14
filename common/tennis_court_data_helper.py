#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/15 01:06
@Author  : claudexie
@File    : tennis_court_data_helper.py
@Software: PyCharm
"""

import json
import requests
import subprocess

import streamlit as st

from common.log_config import setup_logger

# Configure logger
logger = setup_logger(__name__)


def get_realtime_tennis_court_data():
    """
    获取网球场动态数据
    :return:
    """
    data = {}
    try:
        # 发送GET请求到API端点
        api_url = F"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON响应
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"HTTP请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")

    return data
