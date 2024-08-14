#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/15 01:06
@Author  : claudexie
@File    : tennis_court_data_helper.py
@Software: PyCharm
"""

import os
import subprocess

import streamlit as st

from common.log_config import setup_logger

# Configure logger
logger = setup_logger(__name__)


def sync_and_find_files(remote_host, username, remote_path, local_path):
    """
    从远程服务器读取文件数据
    :param remote_host:
    :param username:
    :param remote_path:
    :param local_path:
    :return:
    """
    # 构建 rsync 命令
    rsync_command = [
        'rsync',
        '-avz',
        f'{username}@{remote_host}:{remote_path}',
        local_path
    ]
    # 使用 subprocess 运行 rsync 命令
    result = subprocess.run(rsync_command, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Error syncing files: {result.stderr}")
        return []

    # 遍历本地目录，查找以 available_court.txt 结尾的文件
    matching_files = []
    for root, dirs, files in os.walk(f"/root{local_path}"):
        for file in files:
            if file.endswith('available_court.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    file_content = f.read()
                matching_files.append({
                    'filename': file_path,
                    'content': file_content
                })
    return matching_files


def get_realtime_tennis_court_data():
    """
    获取网球场动态数据
    :return:
    """
    data_file_infos = sync_and_find_files(st.secrets["ZACKS"]["TENNIS_HELPER_HOST_IP"], 'root', "/root", "/tennis")
    st.write(f"data_file_infos: {data_file_infos}")
    return data_file_infos
