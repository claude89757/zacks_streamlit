#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/11 18:52
@Author  : claude
@File    : 1_短信订阅.py
@Software: PyCharm
"""
import time
import os
import datetime
import pandas as pd

import streamlit as st
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="短信订阅", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Render Streamlit pages
st.title("空场短信提醒")

# CSV 文件路径
CSV_FILE_PATH = "subscriptions.csv"

# 订阅的字段
FIELDS = [
    "订阅场地", "开始日期", "结束日期", "开始时间", "结束时间", "最短时长", "订阅状态",
    "今天短信", "累计短信", "手机尾号", "用户等级", "创建时间", "手机号", "昵称"
]

# 订阅场地选项
VENUE_OPTIONS = [
    '大沙河', '深云文体', '深圳湾', '香蜜体育', '莲花体育', '简上', '黄木岗', '华侨城', '福田中心',
    '黄冈公园', '北站公园', '金地威新', '泰尼斯香蜜', '总裁俱乐部', '郑洁俱乐部', '梅林文体', '莲花二村',
    '山花馆', '九龙山', '网羽中心'
]

# 最短时长选项
DURATION_OPTIONS = ['1小时', '2小时', '3小时']

# 检查 CSV 文件是否存在，如果不存在则创建
if not os.path.exists(CSV_FILE_PATH):
    df = pd.DataFrame(columns=FIELDS)
    df.to_csv(CSV_FILE_PATH, index=False)


# 读取 CSV 文件
def read_csv():
    return pd.read_csv(CSV_FILE_PATH)


# 写入 CSV 文件
def write_csv(df):
    df.to_csv(CSV_FILE_PATH, index=False)


# 创建订阅
def create_subscription(data):
    df = read_csv()
    df = df.append(data, ignore_index=True)
    write_csv(df)


# 查询订阅
def query_subscription(phone_suffix):
    df = read_csv()
    return df[df["手机尾号"].str.contains(phone_suffix)]


# 删除订阅
def delete_subscription(phone_number):
    df = read_csv()
    df = df[df["手机号"] != phone_number]
    write_csv(df)


# Streamlit 页面布局
tab1, tab2, tab3 = st.tabs(["创建订阅", "查询订阅", "删除订阅"])

# 创建订阅 TAB
with tab1:
    st.header("创建订阅")
    subscription_data = {}
    subscription_data["订阅场地"] = st.selectbox("订阅场地", VENUE_OPTIONS)
    subscription_data["最短时长"] = st.selectbox("最短时长", DURATION_OPTIONS)
    subscription_data["开始日期"] = st.date_input("开始日期")
    subscription_data["结束日期"] = st.date_input("结束日期")
    subscription_data["开始时间"] = st.time_input("开始时间", value=pd.to_datetime("18:00").time())
    subscription_data["结束时间"] = st.time_input("结束时间")
    subscription_data["手机号"] = st.text_input("手机号")
    subscription_data["昵称"] = st.text_input("昵称（可选）")
    subscription_data["订阅状态"] = "运行中"
    subscription_data["今天短信"] = "-"
    subscription_data["累计短信"] = "-"
    subscription_data["手机尾号"] = subscription_data["手机号"][-4:]
    subscription_data["用户等级"] = "普通"
    subscription_data["创建时间"] = time.strftime("%Y-%m-%d %H:%M:%S")

    if st.button("提交"):
        create_subscription(subscription_data)
        st.success("订阅创建成功！")

# 查询订阅 TAB
with tab2:
    st.header("查询订阅")
    phone_suffix = st.text_input("输入手机尾号")
    if st.button("查询"):
        results = query_subscription(phone_suffix)
        st.write(results)

# 删除订阅 TAB
with tab3:
    st.header("删除订阅")
    phone_number = st.text_input("输入手机号")
    if st.button("查询订阅"):
        results = query_subscription(phone_number[-4:])
        selected_subscription = st.selectbox("选择要删除的订阅", results.index)
        if st.button("删除"):
            delete_subscription(results.loc[selected_subscription, "手机号"])
            st.success("订阅删除成功！")
