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
from filelock import FileLock
import uuid


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
LOCK_FILE_PATH = "subscriptions.csv.lock"


# 初始化 session state
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ''
if 'results' not in st.session_state:
    st.session_state.results = pd.DataFrame()
if 'selected_subscriptions' not in st.session_state:
    st.session_state.selected_subscriptions = []
if 'del_subscription_id' not in st.session_state:
    st.session_state.del_subscription_id = st.query_params.get('del_subscription_id', "")


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


# 检查 CSV 文件是否存在，如果不存在则创建
if not os.path.exists(CSV_FILE_PATH):
    df = pd.DataFrame(columns=FIELDS)
    df.to_csv(CSV_FILE_PATH, index=False)


# 检查 CSV 文件是否存在，如果不存在则创建
if not os.path.exists(CSV_FILE_PATH):
    df = pd.DataFrame(columns=FIELDS)
    df.to_csv(CSV_FILE_PATH, index=False)


# 读取 CSV 文件
def read_csv():
    with FileLock(LOCK_FILE_PATH):
        return pd.read_csv(CSV_FILE_PATH)


# 写入 CSV 文件
def write_csv(df):
    with FileLock(LOCK_FILE_PATH):
        df.to_csv(CSV_FILE_PATH, index=False)


# 创建订阅
def create_subscription(data):
    df = read_csv()
    data["订阅ID"] = str(uuid.uuid4())  # 生成唯一的订阅ID
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    write_csv(df)


# 查询订阅
def query_subscription(phone_number):
    df = read_csv()
    df["手机号"] = df["手机号"].astype(str)  # 确保手机号列为字符串类型
    results = df[df["手机号"].str.contains(phone_number)]
    return results


# 删除订阅
def delete_subscription(subscription_id):
    st.write(f"deleting ...{subscription_id}")
    with FileLock(LOCK_FILE_PATH):
        df = read_csv()
        st.dataframe(df.head(100))
        df = df[df["订阅ID"] != subscription_id]
        st.dataframe(df.head(100))
        write_csv(df)


# Streamlit 页面布局
tab1, tab2 = st.tabs(["创建订阅", "查询订阅"])

# 创建订阅 TAB
with tab1:
    st.header("创建订阅")
    subscription_data = {}

    col1, col2 = st.columns(2)
    with col1:
        subscription_data["订阅场地"] = st.selectbox("订阅场地", VENUE_OPTIONS)
    with col2:
        subscription_data["最短时长"] = st.selectbox("最短时长", DURATION_OPTIONS)

    col3, col4 = st.columns(2)
    with col3:
        subscription_data["开始日期"] = st.date_input("开始日期")
    with col4:
        subscription_data["结束日期"] = st.date_input("结束日期")

    col5, col6 = st.columns(2)
    with col5:
        subscription_data["开始时间"] = st.time_input("开始时间", value=pd.to_datetime("18:00").time())
    with col6:
        subscription_data["结束时间"] = st.time_input("结束时间", value=pd.to_datetime("22:00").time())

    col7, col8 = st.columns(2)
    with col7:
        subscription_data["手机号"] = st.text_input("手机号", value=st.session_state.phone_number)
    with col8:
        subscription_data["昵称"] = st.text_input("昵称（可选）")

    subscription_data["订阅状态"] = "运行中"
    subscription_data["今天短信"] = "-"
    subscription_data["累计短信"] = "-"
    subscription_data["手机尾号"] = subscription_data["手机号"][-4:]
    subscription_data["用户等级"] = "VIP"
    subscription_data["创建时间"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # 提交按钮
    if st.button("创建订阅", key="submit_button", help="点击提交订阅信息", type="primary"):
        # 手机号验证
        if not subscription_data["手机号"].isdigit() or len(subscription_data["手机号"]) != 11:
            st.error("请输入有效的11位手机号")
        else:
            create_subscription(subscription_data)
            value = st.session_state.phone_number = subscription_data["手机号"]
            st.balloons()
            st.success("订阅创建成功！请关注手机短信提醒。")

st.write(f"del_subscription_id: {st.session_state.del_subscription_id}")

# 查询订阅 TAB
with tab2:
    if st.session_state.del_subscription_id:
        delete_subscription(st.session_state.del_subscription_id)
        st.success(f"订阅  {st.session_state.del_subscription_id} 已删除")
        st.session_state.del_subscription_id = ""
        st.query_params.del_subscription_id = ""
    st.header("查询订阅")
    phone_number = st.text_input("输入手机", value=st.session_state.phone_number)
    st.session_state.phone_number = phone_number
    if not subscription_data["手机号"].isdigit() or len(subscription_data["手机号"]) != 11:
        st.error("请输入有效的11位手机号")
        time.sleep(1)
        st.rerun()
    else:
        if st.button("查询订阅", key="query_button_01"):
            results = query_subscription(phone_number)
            if results.empty:
                st.warning("未找到相关订阅信息，请检查手机号是否正确。")
            else:
                for index, row in results.iterrows():
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander(f"订阅 {index + 1}: {row['订阅场地']} {row['订阅状态']}"):
                            st.write(f"**开始日期**: {row['开始日期']}")
                            st.write(f"**结束日期**: {row['结束日期']}")
                            st.write(f"**开始时间**: {row['开始时间']}")
                            st.write(f"**结束时间**: {row['结束时间']}")
                            st.write(f"**最短时长**: {row['最短时长']}")
                            st.write(f"**今天短信**: {row['今天短信']}")
                            st.write(f"**累计短信**: {row['累计短信']}")
                            st.write(f"**手机尾号**: {row['手机尾号']}")
                            st.write(f"**用户等级**: {row['用户等级']}")
                            st.write(f"**创建时间**: {row['创建时间']}")
                            st.write(f"**昵称**: {row['昵称']}")
                    with col2:
                        # 删除按钮
                        st.write(f"订阅ID: {row['订阅ID']}")
                        if st.button(f"删除订阅 {index + 1}", key=f"delete_button_{index}", type="primary"):
                            st.query_params.del_subscription_id = row['订阅ID']
                            st.session_state.del_subscription_id = row['订阅ID']
                            time.sleep(3)
                            st.rerun()
