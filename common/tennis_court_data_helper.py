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


def find_files_in_local_directory(local_path):
    # 遍历本地目录，查找以 available_court.txt 结尾的文件
    matching_files = []
    for root, dirs, files in os.walk(local_path):
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
    data_file_infos = find_files_in_local_directory("/root")
    return data_file_infos

