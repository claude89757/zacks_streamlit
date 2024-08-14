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
    data_file_infos = {}
    try:
        # 发送GET请求到API端点
        api_url = F"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON响应
        data = response.json()

        # 遍历每个文件的信息
        for file_info in data:
            filename = file_info.get('filename')
            content = file_info.get('content')

            # 解析文件内容中的JSON字符串
            parsed_content = json.loads(content)

            print(f"Filename: {filename}")
            print("Content:")
            print(json.dumps(parsed_content, indent=4, ensure_ascii=False))  # 美化输出

            data_file_infos = parsed_content

    except requests.exceptions.RequestException as e:
        print(f"HTTP请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")

    st.write(f"data_file_infos: {data_file_infos}")
    return data_file_infos
