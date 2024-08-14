#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/15 01:06
@Author  : claudexie
@File    : tennis_court_data_helper.py
@Software: PyCharm
"""

import requests
import json
import streamlit as st


def format_data_for_markdown(data):
    markdown = ""
    for item in data:
        # Parse the JSON content
        try:
            content = json.loads(item['content'])
        except json.JSONDecodeError as e:
            st.error(f"JSON解析错误: {e}")
            continue

        for date, courts in content.items():
            markdown += f"### {date}\n\n"
            markdown += "| Court ID | Time Slots |\n"
            markdown += "|----------|------------|\n"
            for court_id, slots in courts.items():
                slots_str = ', '.join([f"{start} - {end}" for start, end in slots])
                markdown += f"| {court_id} | {slots_str} |\n"
            markdown += "\n"
    return markdown


def get_realtime_tennis_court_data():
    """
    获取网球场动态数据
    :return:
    """
    data = []
    try:
        # 发送GET请求到API端点
        api_url = F"http://{st.secrets['ZACKS']['TENNIS_HELPER_HOST_IP']}:5000/api/files"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON响应
        data = response.json()

        # 格式化数据为Markdown
        markdown_data = format_data_for_markdown(data)
        st.markdown(markdown_data)

    except requests.exceptions.RequestException as e:
        st.error(f"HTTP请求错误: {e}")
    except json.JSONDecodeError as e:
        st.error(f"JSON解析错误: {e}")




