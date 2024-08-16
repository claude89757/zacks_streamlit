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
import pandas as pd
from filelock import FileLock
import streamlit as st
from common.log_config import setup_logger
from common.settings import common_settings_init
from common.redis_client import RedisClient
from sidebar import sidebar
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

# 初始化 session state
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ''
if "redis_client" not in st.session_state:
    st.session_state.redis_client = RedisClient()

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


KEY_MAPPING = {
    'owner': '拥有者',
    'end_date': '结束日期',
    'jrtzcs': '今日通知次数',
    'tzgq': '通知过期',
    '_departmentList': '部门列表',
    'end_time': '结束时间',
    'cdhm': '场地号',
    'xjcd': '订阅场地',
    'duration': '时长',
    'createdAt': '创建时间',
    'start_time': '开始时间',
    'sfsd': '是否收到',
    'createBy': '创建者',
    'updateBy': '更新者',
    'phone': '手机号码',
    'name': '昵称',
    'user_level': '用户等级',
    '_id': '订阅ID',
    'sjwh': '手机尾号',
    'zjtzcs': '总计通知次数',
    'updatedAt': '更新时间',
    'start_date': '开始日期',
    'status': '状态'
}


REVERSE_KEY_MAPPING = {
    '拥有者': 'owner',
    '结束日期': 'end_date',
    '今日通知次数': 'jrtzcs',
    '通知过期': 'tzgq',
    '部门列表': '_departmentList',
    '结束时间': 'end_time',
    '场地号': 'cdhm',
    '订阅场地': 'xjcd',
    '时长': 'duration',
    '创建时间': 'createdAt',
    '开始时间': 'start_time',
    '是否收到': 'sfsd',
    '创建者': 'createBy',
    '更新者': 'updateBy',
    '手机号码': 'phone',
    '昵称': 'name',
    '用户等级': 'user_level',
    '订阅ID': '_id',
    '手机尾号': 'sjwh',
    '总计通知次数': 'zjtzcs',
    '更新时间': 'updatedAt',
    '开始日期': 'start_date',
    '状态': 'status'
}


# 最短时长选项
DURATION_OPTIONS = ['1小时', '2小时', '3小时']

# Redis 键名
REDIS_KEY = "subscriptions"


# 创建订阅
def create_subscription(data):
    with st.spinner("creating subscription..."):
        data["_id"] = str(uuid.uuid4())  # 生成唯一的订阅ID
        subscription_list = st.session_state.redis_client.get_json_data(REDIS_KEY, use_lock=True) or []
        subscription_list.append(data)
        st.session_state.redis_client.set_json_data(REDIS_KEY, subscription_list, use_lock=True)
        time.sleep(3)


# 查询订阅
def query_subscription(phone_number):
    with st.spinner("querying subscription..."):
        subscription_list = st.session_state.redis_client.get_json_data(REDIS_KEY) or []
        results = [sub for sub in subscription_list if sub["phone"].startswith(phone_number)]
        time.sleep(1)
        return results


# 删除订阅
def delete_subscription(subscription_id):
    with st.spinner("deleting subscription..."):
        subscription_list = st.session_state.redis_client.get_json_data(REDIS_KEY) or []
        subscription_list = [sub for sub in subscription_list if sub["_id"] != subscription_id]
        st.session_state.redis_client.set_json_data(REDIS_KEY, subscription_list, use_lock=True)
        time.sleep(1)


# 页面布局
tab1, tab2 = st.tabs(["创建订阅", "查询订阅"])

# 创建订阅 TAB
with tab1:
    st.header("创建订阅")
    subscription_data = {}

    col1, col2 = st.columns(2)
    with col1:
        subscription_data["xjcd"] = st.selectbox("订阅场地", VENUE_OPTIONS)
    with col2:
        subscription_data["duration"] = st.selectbox("最短时长", DURATION_OPTIONS)

    col3, col4 = st.columns(2)
    with col3:
        subscription_data["start_date"] = st.date_input("开始日期")
    with col4:
        subscription_data["end_date"] = st.date_input("结束日期")

    col5, col6 = st.columns(2)
    with col5:
        subscription_data["start_time"] = st.time_input("开始时间", value=pd.to_datetime("18:00").time())
    with col6:
        subscription_data["end_time"] = st.time_input("结束时间", value=pd.to_datetime("22:00").time())

    col7, col8 = st.columns(2)
    with col7:
        subscription_data["phone"] = st.text_input("手机号", value=st.session_state.phone_number)
    with col8:
        subscription_data["name"] = st.text_input("昵称（可选）")

    subscription_data["start_date"] = subscription_data["start_date"].strftime("%Y-%m-%d")
    subscription_data["end_date"] = subscription_data["end_date"].strftime("%Y-%m-%d")
    subscription_data["start_time"] = subscription_data["start_time"].strftime("%H:%M")
    subscription_data["end_time"] = subscription_data["end_time"].strftime("%H:%M")
    subscription_data["status"] = "运行中"
    subscription_data["jrtzcs"] = 0
    subscription_data["zjtzcs"] = 0
    subscription_data["sjwh"] = subscription_data["phone"][-4:]
    subscription_data["user_level"] = "VIP"
    subscription_data["createdAt"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # 提交按钮
    if st.button("创建订阅", key="submit_button", help="点击提交订阅信息", type="primary"):
        # 手机号验证
        if not subscription_data["phone"].isdigit() or len(subscription_data["phone"]) != 11:
            st.error("请输入有效的11位手机号")
        else:
            # 统计数据
            sidebar()
            # Redis 操作
            create_subscription(subscription_data)
            value = st.session_state.phone_number = subscription_data["phone"]
            st.balloons()
            st.success("订阅创建成功！请关注手机短信提醒。")

# 查询订阅 TAB
with tab2:
    st.header("查询订阅")
    phone_number = st.text_input("输入手机", value=st.session_state.phone_number)
    st.session_state.phone_number = phone_number

    if st.button("查询订阅", key="query_button_01"):
        if not st.session_state.phone_number or len(st.session_state.phone_number) != 11:
            st.error("请输入有效的11位手机号")
            time.sleep(2)
            st.rerun()
        else:
            pass
    if st.session_state.phone_number:
        results = query_subscription(st.session_state.phone_number)
        if not results:
            st.warning("未找到相关订阅信息，请检查手机号是否正确。")
        else:
            for index, row in enumerate(results):
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander(f"订阅 {index + 1}: {row['xjcd']} {row['status']}"):
                        st.write(f"**开始日期**: {row['start_date']}")
                        st.write(f"**结束日期**: {row['end_date']}")
                        st.write(f"**开始时间**: {row['start_time']}")
                        st.write(f"**结束时间**: {row['end_time']}")
                        st.write(f"**最短时长**: {row['duration']}")
                        st.write(f"**今天短信**: {row['jrtzcs']}")
                        st.write(f"**累计短信**: {row['zjtzcs']}")
                        st.write(f"**手机尾号**: {row['sjwh']}")
                        st.write(f"**用户等级**: {row['user_level']}")
                        st.write(f"**创建时间**: {row['createdAt']}")
                        st.write(f"**昵称**: {row['name']}")

                with col2:
                    if 'selected_subscription_id' not in st.session_state:
                        st.session_state.selected_subscription_id = None
                    st.session_state.selected_subscription_id = row["_id"]
                    # Only delete if button is clicked
                    if st.button("删除订阅", key=f"delete_button_{index}"):
                        if st.session_state.selected_subscription_id:
                            delete_subscription(st.session_state.selected_subscription_id)
                            st.session_state.selected_subscription_id = None  # Clear the selection
                            st.success("订阅删除成功！")
                            st.rerun()  # Refresh page to update subscription lis
